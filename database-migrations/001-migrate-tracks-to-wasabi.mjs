/**
 * Migrate tracks from Contabo S3 to Wasabi S3
 *
 * 1. Update 'url' and 'normalizedAudioUrl' fields in 'library-tracks-v0001'
 *    collection to point to Wasabi S3 instead of public link in Contabo S3
 * 2. Add 'version' to migrated documents to track migration status and
 *    backward compatibility in future migrations.
 */

import PouchDB from 'pouchdb';

// Check if REMOTE_DATABASE_URL is set
const REMOTE_DATABSE_URL = process.env.REMOTE_DATABASE_URL;
if (!REMOTE_DATABSE_URL) {
  console.error('REMOTE_DATABASE_URL is required');
  process.exit(1);
}

// Database name to migrate
const databaseName = 'library-tracks-v0001';
const remoteDB = new PouchDB(REMOTE_DATABSE_URL + "/database/" + databaseName);
const localDB = new PouchDB("./db/" + databaseName);

/* -------------------------------------------------------------------------- */
/*                                  Functions                                 */
/* -------------------------------------------------------------------------- */

async function replicateDatabase(sourceDB, targetDB) {
  try {
    await targetDB.replicate.from(sourceDB);
    console.log('Replication complete');
  } catch (error) {
    console.error('Replication failed:', error);
  }
}

async function getDocumentsToMigrate(db) {
  const docs = await db.allDocs({ include_docs: true });
  return docs.rows
    .filter(doc => !doc.id.startsWith('_'))
    .filter(doc => doc.doc.version === undefined)
    .map(x => x.doc);
}

/* -------------------------------------------------------------------------- */
/*                                   Actions                                  */
/* -------------------------------------------------------------------------- */

await replicateDatabase(remoteDB, localDB)
const documentsToMigrate = await getDocumentsToMigrate(localDB);

for (const doc of documentsToMigrate) {
  const base = "https://eu2.contabostorage.com/79a9f6821486456a8b803a47e4bf205f:library"
  const audioOriginalUrl =
    doc.url.startsWith(`${base}/original/`)
      ? doc.url.replace(`${base}/original/`, "library/audio/original/")
      : doc.url.replace(`${base}/`, "library/audio/original/")

  const audioNormalizedUrl =
    doc.audioNormalizedUrl
      ? doc.audioNormalizedUrl.replace(`${base}/normalized`, "library/audio/normalized")
      : undefined

  const audioUrl = {
    original: audioOriginalUrl,
    normalized: audioNormalizedUrl
  }
  if (!audioUrl.normalized) { delete audioUrl.normalized }

  doc.version = 1
  doc.audioUrl = audioUrl

  delete doc.url
  delete doc.audioNormalizedUrl

  localDB.put(doc)
  console.log(doc)
}
await replicateDatabase(localDB, remoteDB)