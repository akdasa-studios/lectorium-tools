var PouchDB = require('pouchdb')
  .plugin(require('pouchdb-adapter-node-websql'))

const baseUri  = process.env.DATABASE_URI
const databases = [
  'library-dictionary-v0001',
  'library-tracks-v0001',
  'library-index-v0001',
]

for (const database of databases) {
  console.log(`Processing ${database}...`)
  const inputDB  = new PouchDB(`${baseUri}${database}`)
  const outputDB = new PouchDB(`./artifacts/${database}.db`, { adapter: 'websql' })

  inputDB.replicate.to(
    outputDB, {
      filter: (doc) => !doc._id.startsWith('_')
    }
  ).then((result) => {
    console.log("Replication succeeded:", result);
  }).catch((error) => {
    console.error("Replication failed:", error);
  });
}
