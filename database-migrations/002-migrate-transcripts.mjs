/**
 * Migrate transcripts to new format
 *
 * 1. Move `text.blocks` field to `blocks` field. Because nesting `blocks`
 *    under `text` doesn't make sense.
 * 2. Add `version` to migrated documents to track migration status and
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
const databaseName = 'library-transcripts-v0001';
const remoteDB = new PouchDB(REMOTE_DATABSE_URL + "database/" + databaseName);
const localDB = new PouchDB("./db/" + databaseName);

/* -------------------------------------------------------------------------- */
/*                                  Functions                                 */
/* -------------------------------------------------------------------------- */

async function replicateDatabase(sourceDB, targetDB) {
    try {
        await targetDB.replicate.from(sourceDB, { batch_size: 10 });
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

// await replicateDatabase(remoteDB, localDB)
const documentsToMigrate = await getDocumentsToMigrate(localDB);

for (const doc of documentsToMigrate) {
    const result = {...doc}
    result.version = 1
    result.blocks = doc.text.blocks
    delete result.text

    console.log(result)
    await localDB.put(result)
}
await replicateDatabase(localDB, remoteDB)