Yes, you can use Prisma to load data into MongoDB. Prisma is an ORM (Object-Relational Mapping) tool that supports various databases, including MongoDB. It allows you to define your data models in a schema file and provides a type-safe API to interact with your database.

### Steps to Set Up Prisma with MongoDB

1. **Install Prisma CLI**:
   ```sh
   npm install @prisma/cli --save-dev
   ```

2. **Initialize Prisma**:
   ```sh
   npx prisma init
   ```

   This command will create a `prisma` directory with a `schema.prisma` file and a `.env` file.

3. **Configure MongoDB in `.env`**:
   Update the `.env` file with your MongoDB connection string:

   ```plaintext
   DATABASE_URL="mongodb://localhost:27017/quizAppDB"
   ```

4. **Update `schema.prisma`**:
   Modify the `schema.prisma` file to define your data models. Here’s an example schema for a quiz application:

   ```prisma
   datasource db {
     provider = "mongodb"
     url      = env("DATABASE_URL")
   }

   generator client {
     provider = "prisma-client-js"
   }

   model Quiz {
     id            String   @id @default(auto()) @map("_id") @db.ObjectId
     question      String
     answers       String[]
     correctAnswer String
     category      String
     difficulty    String
   }
   ```

5. **Generate Prisma Client**:
   Run the following command to generate the Prisma Client based on your schema:

   ```sh
   npx prisma generate
   ```

6. **Use Prisma Client in Your Application**:
   You can now use the Prisma Client to interact with your MongoDB database. Here’s an example of how to use it in your application:

   ```javascript
   // prisma/seed.js
   const { PrismaClient } = require('@prisma/client');
   const prisma = new PrismaClient();

   async function main() {
     await prisma.quiz.create({
       data: {
         question: 'What is the capital of France?',
         answers: ['Paris', 'London', 'Berlin', 'Madrid'],
         correctAnswer: 'Paris',
         category: 'Geography',
         difficulty: 'Easy',
       },
     });

     const allQuizzes = await prisma.quiz.findMany();
     console.log(allQuizzes);
   }

   main()
     .catch((e) => {
       throw e;
     })
     .finally(async () => {
       await prisma.$disconnect();
     });
   ```

7. **Run the Seed Script**:
   Execute the seed script to load data into MongoDB:

   ```sh
   node prisma/seed.js
   ```

### Example of Using Prisma in an Express Route

1. **Install Prisma Client**:
   ```sh
   npm install @prisma/client
   ```

2. **Create Routes to Interact with the Database**:
   Update your `quizRoutes.js` file to include routes for creating and fetching quiz questions using Prisma:

   ```javascript
   // routes/quizRoutes.js
   const express = require('express');
   const router = express.Router();
   const { PrismaClient } = require('@prisma/client');
   const prisma = new PrismaClient();

   // Route to get all quiz questions
   router.get('/questions', async (req, res) => {
     try {
       const questions = await prisma.quiz.findMany();
       res.json(questions);
     } catch (error) {
       console.error(error);
       res.status(500).json({ message: 'Server error' });
     }
   });

   // Route to add a new quiz question
   router.post('/add-quiz', async (req, res) => {
     try {
       const { question, answers, correctAnswer, category, difficulty } = req.body;

       const newQuiz = await prisma.quiz.create({
         data: {
           question,
           answers,
           correctAnswer,
           category,
           difficulty,
         },
       });

       res.status(201).json({ message: 'Quiz question added successfully', newQuiz });
     } catch (error) {
       console.error(error);
       res.status(500).json({ message: 'Server error' });
     }
   });

   module.exports = router;
   ```

### Summary

By following these steps, you can set up Prisma with MongoDB and use it to load data into your database. Prisma provides a type-safe API to interact with your database, making it easier to manage your data models and perform database operations.

---

# Run mongodb as replicaset

Prisma requires your MongoDB server to be run as a replica set to perform transactions. This is a common requirement for using transactions with MongoDB in Prisma.

### Steps to Resolve:

1. **Configure MongoDB as a Replica Set**:
   - You need to start your MongoDB server with replica set configuration.

### Example for Local MongoDB Setup:

1. **Stop MongoDB Service** (if running):
   ```sh
   brew services stop mongodb/brew/mongodb-community
   ```

2. **Start MongoDB with Replica Set**:
   ```sh
   mongod --replSet rs0 --bind_ip localhost
   ```

3. **Initialize the Replica Set**:
   - Open a new terminal and connect to MongoDB shell:
     ```sh
     mongo
     ```
   - Run the following commands in the MongoDB shell:
     ```javascript
     rs.initiate()
     ```

### Example for Docker Setup:

1. **Create a Docker Compose File** (`docker-compose.yml`):
   ```yaml
   version: '3.8'
   services:
     mongo:
       image: mongo:latest
       command: ["mongod", "--replSet", "rs0"]
       ports:
         - "27017:27017"
   ```

2. **Start the Docker Container**:
   ```sh
   docker-compose up -d
   ```

3. **Initialize the Replica Set**:
   - Connect to the MongoDB container:
     ```sh
     docker exec -it <container_id> mongo
     ```
   - Run the following commands in the MongoDB shell:
     ```javascript
     rs.initiate()
     ```

### Verify the Setup:

1. **Check Replica Set Status**:
   - In the MongoDB shell, run:
     ```javascript
     rs.status()
     ```

2. **Run Your Prisma Seed Script Again**:
   ```sh
   node prisma/seed.js
   ```

### Summary:

- **Stop MongoDB Service**: Ensure MongoDB is not running as a standalone instance.
- **Start MongoDB with Replica Set**: Use the `--replSet` option.
- **Initialize Replica Set**: Use `rs.initiate()` in the MongoDB shell.
- **Verify Setup**: Check the replica set status.
- **Run Prisma Seed Script**: Retry the seed script.

This should resolve the error and allow Prisma to perform transactions with your MongoDB instance.

---

## Setup Data directory

The error message indicates that MongoDB failed to start because the data directory `/data/db` does not exist. You need to create this directory or specify a different path for the database files.

### Steps to Resolve:

1. **Create the Data Directory**:
   - You can create the `/data/db` directory with the following command:
     ```sh
     sudo mkdir -p /data/db
     sudo chown -R `id -u` /data/db
     ```

2. **Specify a Different Data Directory**:
   - Alternatively, you can specify a different path for the database files using the `--dbpath` option.

### Example for Specifying a Different Data Directory:

1. **Create a Custom Data Directory**:
   - Create a directory in your home directory or another location:
     ```sh
     mkdir -p ~/mongodb/data/db
     ```

2. **Start MongoDB with the Custom Data Directory**:
   - Use the `--dbpath` option to specify the custom data directory:
     ```sh
     mongod --dbpath ~/mongodb/data/db --replSet rs0
     ```

3. **Initialize the Replica Set**:
   - Open a new terminal and connect to the MongoDB shell:
     ```sh
     mongo
     ```
   - Run the following command in the MongoDB shell:
     ```javascript
     rs.initiate()
     ```

### Verify the Setup:

1. **Check Replica Set Status**:
   - In the MongoDB shell, run:
     ```javascript
     rs.status()
     ```

2. **Run Your Prisma Seed Script Again**:
   ```sh
   node prisma/seed.js
   ```

### Summary:

- **Create Data Directory**: Ensure the data directory exists and has the correct permissions.
- **Specify Custom Data Directory**: Use the `--dbpath` option if you prefer a different location.
- **Start MongoDB with Replica Set**: Use the `--replSet` option.
- **Initialize Replica Set**: Use `rs.initiate()` in the MongoDB shell.
- **Verify Setup**: Check the replica set status.
- **Run Prisma Seed Script**: Retry the seed script.

This should resolve the issue and allow MongoDB to start correctly.

---

```
gsaravanan@gs-mac-pro backend % mongod --dbpath ~/mongodb/data/db --replSet rs0 --bind_ip localhost
{"t":{"$date":"2024-10-09T23:16:00.538+05:30"},"s":"I",  "c":"CONTROL",  "id":23285,   "ctx":"thread2","msg":"Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'"}
{"t":{"$date":"2024-10-09T23:16:00.540+05:30"},"s":"I",  "c":"NETWORK",  "id":4915701, "ctx":"thread2","msg":"Initialized wire specification","attr":{"spec":{"incomingExternalClient":{"minWireVersion":0,"maxWireVersion":13},"incomingInternalClient":{"minWireVersion":0,"maxWireVersion":13},"outgoing":{"minWireVersion":0,"maxWireVersion":13},"isInternalClient":true}}}
{"t":{"$date":"2024-10-09T23:16:00.564+05:30"},"s":"W",  "c":"ASIO",     "id":22601,   "ctx":"thread2","msg":"No TransportLayer configured during NetworkInterface startup"}
{"t":{"$date":"2024-10-09T23:16:00.565+05:30"},"s":"I",  "c":"NETWORK",  "id":4648602, "ctx":"thread2","msg":"Implicit TCP FastOpen in use."}
{"t":{"$date":"2024-10-09T23:16:00.570+05:30"},"s":"W",  "c":"ASIO",     "id":22601,   "ctx":"thread2","msg":"No TransportLayer configured during NetworkInterface startup"}
{"t":{"$date":"2024-10-09T23:16:00.571+05:30"},"s":"W",  "c":"ASIO",     "id":22601,   "ctx":"thread2","msg":"No TransportLayer configured during NetworkInterface startup"}
{"t":{"$date":"2024-10-09T23:16:00.572+05:30"},"s":"I",  "c":"REPL",     "id":5123008, "ctx":"thread2","msg":"Successfully registered PrimaryOnlyService","attr":{"service":"TenantMigrationDonorService","ns":"config.tenantMigrationDonors"}}
{"t":{"$date":"2024-10-09T23:16:00.572+05:30"},"s":"I",  "c":"REPL",     "id":5123008, "ctx":"thread2","msg":"Successfully registered PrimaryOnlyService","attr":{"service":"TenantMigrationRecipientService","ns":"config.tenantMigrationRecipients"}}
{"t":{"$date":"2024-10-09T23:16:00.572+05:30"},"s":"I",  "c":"CONTROL",  "id":5945603, "ctx":"thread2","msg":"Multi threading initialized"}
{"t":{"$date":"2024-10-09T23:16:00.572+05:30"},"s":"I",  "c":"CONTROL",  "id":4615611, "ctx":"initandlisten","msg":"MongoDB starting","attr":{"pid":34446,"port":27017,"dbPath":"/Users/gsaravanan/mongodb/data/db","architecture":"64-bit","host":"gs-mac-pro.local"}}
{"t":{"$date":"2024-10-09T23:16:00.572+05:30"},"s":"I",  "c":"CONTROL",  "id":23403,   "ctx":"initandlisten","msg":"Build Info","attr":{"buildInfo":{"version":"5.0.29","gitVersion":"cd239f3b0c7796df9e576ae5a9efcf4e6960560c","modules":[],"allocator":"system","environment":{"distarch":"x86_64","target_arch":"x86_64"}}}}
{"t":{"$date":"2024-10-09T23:16:00.572+05:30"},"s":"I",  "c":"CONTROL",  "id":51765,   "ctx":"initandlisten","msg":"Operating System","attr":{"os":{"name":"Mac OS X","version":"24.1.0"}}}
{"t":{"$date":"2024-10-09T23:16:00.572+05:30"},"s":"I",  "c":"CONTROL",  "id":21951,   "ctx":"initandlisten","msg":"Options set by command line","attr":{"options":{"net":{"bindIp":"localhost"},"replication":{"replSet":"rs0"},"storage":{"dbPath":"/Users/gsaravanan/mongodb/data/db"}}}}
{"t":{"$date":"2024-10-09T23:16:00.581+05:30"},"s":"I",  "c":"NETWORK",  "id":5693100, "ctx":"initandlisten","msg":"Asio socket.set_option failed with std::system_error","attr":{"note":"acceptor TCP fast open","option":{"level":6,"name":261,"data":"00 04 00 00"},"error":{"what":"set_option: Invalid argument","message":"Invalid argument","category":"asio.system","value":22}}}
{"t":{"$date":"2024-10-09T23:16:00.583+05:30"},"s":"I",  "c":"STORAGE",  "id":22270,   "ctx":"initandlisten","msg":"Storage engine to use detected by data files","attr":{"dbpath":"/Users/gsaravanan/mongodb/data/db","storageEngine":"wiredTiger"}}
{"t":{"$date":"2024-10-09T23:16:00.583+05:30"},"s":"I",  "c":"STORAGE",  "id":22315,   "ctx":"initandlisten","msg":"Opening WiredTiger","attr":{"config":"create,cache_size=3584M,session_max=33000,eviction=(threads_min=4,threads_max=4),config_base=false,statistics=(fast),log=(enabled=true,archive=true,path=journal,compressor=snappy),builtin_extension_config=(zstd=(compression_level=6)),file_manager=(close_idle_time=600,close_scan_interval=10,close_handle_minimum=2000),statistics_log=(wait=0),verbose=[recovery_progress,checkpoint_progress,compact_progress],"}}
{"t":{"$date":"2024-10-09T23:16:01.632+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:632169][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] Recovering log 2 through 3"}}
{"t":{"$date":"2024-10-09T23:16:01.713+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:713120][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] Recovering log 3 through 3"}}
{"t":{"$date":"2024-10-09T23:16:01.768+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:768841][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_ALL] Main recovery loop: starting at 2/254336 to 3/256"}}
{"t":{"$date":"2024-10-09T23:16:01.843+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:843257][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] Recovering log 2 through 3"}}
{"t":{"$date":"2024-10-09T23:16:01.887+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:887712][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] Recovering log 3 through 3"}}
{"t":{"$date":"2024-10-09T23:16:01.924+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:924901][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] recovery log replay has successfully finished and ran for 293 milliseconds"}}
{"t":{"$date":"2024-10-09T23:16:01.925+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:925299][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_ALL] Set global recovery timestamp: (1728495947, 1)"}}
{"t":{"$date":"2024-10-09T23:16:01.925+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:925347][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_ALL] Set global oldest timestamp: (1728495647, 1)"}}
{"t":{"$date":"2024-10-09T23:16:01.926+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:926597][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] recovery rollback to stable has successfully finished and ran for 1 milliseconds"}}
{"t":{"$date":"2024-10-09T23:16:01.930+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:930121][34446:0x20a30e200], WT_SESSION.checkpoint: [WT_VERB_CHECKPOINT_PROGRESS] saving checkpoint snapshot min: 1, snapshot max: 1 snapshot count: 0, oldest timestamp: (1728495647, 1) , meta checkpoint timestamp: (1728495947, 1) base write gen: 239"}}
{"t":{"$date":"2024-10-09T23:16:01.949+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:949650][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] recovery checkpoint has successfully finished and ran for 22 milliseconds"}}
{"t":{"$date":"2024-10-09T23:16:01.949+05:30"},"s":"I",  "c":"STORAGE",  "id":22430,   "ctx":"initandlisten","msg":"WiredTiger message","attr":{"message":"[1728495961:949720][34446:0x20a30e200], txn-recover: [WT_VERB_RECOVERY_PROGRESS] recovery was completed successfully and took 318ms, including 293ms for the log replay, 1ms for the rollback to stable, and 22ms for the checkpoint."}}
{"t":{"$date":"2024-10-09T23:16:01.954+05:30"},"s":"I",  "c":"STORAGE",  "id":4795906, "ctx":"initandlisten","msg":"WiredTiger opened","attr":{"durationMillis":1370}}
{"t":{"$date":"2024-10-09T23:16:01.954+05:30"},"s":"I",  "c":"RECOVERY", "id":23987,   "ctx":"initandlisten","msg":"WiredTiger recoveryTimestamp","attr":{"recoveryTimestamp":{"$timestamp":{"t":1728495947,"i":1}}}}
{"t":{"$date":"2024-10-09T23:16:01.954+05:30"},"s":"I",  "c":"RECOVERY", "id":5380106, "ctx":"initandlisten","msg":"WiredTiger oldestTimestamp","attr":{"oldestTimestamp":{"$timestamp":{"t":1728495647,"i":1}}}}
{"t":{"$date":"2024-10-09T23:16:01.966+05:30"},"s":"I",  "c":"STORAGE",  "id":22383,   "ctx":"initandlisten","msg":"The size storer reports that the oplog contains","attr":{"numRecords":266,"dataSize":30382}}
{"t":{"$date":"2024-10-09T23:16:01.966+05:30"},"s":"I",  "c":"STORAGE",  "id":22384,   "ctx":"initandlisten","msg":"Scanning the oplog to determine where to place markers for truncation"}
{"t":{"$date":"2024-10-09T23:16:01.967+05:30"},"s":"I",  "c":"STORAGE",  "id":22382,   "ctx":"initandlisten","msg":"WiredTiger record store oplog processing finished","attr":{"durationMillis":1}}
{"t":{"$date":"2024-10-09T23:16:01.972+05:30"},"s":"I",  "c":"STORAGE",  "id":22262,   "ctx":"initandlisten","msg":"Timestamp monitor starting"}
{"t":{"$date":"2024-10-09T23:16:01.972+05:30"},"s":"W",  "c":"CONTROL",  "id":22120,   "ctx":"initandlisten","msg":"Access control is not enabled for the database. Read and write access to data and configuration is unrestricted","tags":["startupWarnings"]}
{"t":{"$date":"2024-10-09T23:16:01.984+05:30"},"s":"I",  "c":"NETWORK",  "id":4915702, "ctx":"initandlisten","msg":"Updated wire specification","attr":{"oldSpec":{"incomingExternalClient":{"minWireVersion":0,"maxWireVersion":13},"incomingInternalClient":{"minWireVersion":0,"maxWireVersion":13},"outgoing":{"minWireVersion":0,"maxWireVersion":13},"isInternalClient":true},"newSpec":{"incomingExternalClient":{"minWireVersion":0,"maxWireVersion":13},"incomingInternalClient":{"minWireVersion":13,"maxWireVersion":13},"outgoing":{"minWireVersion":13,"maxWireVersion":13},"isInternalClient":true}}}
{"t":{"$date":"2024-10-09T23:16:01.984+05:30"},"s":"I",  "c":"STORAGE",  "id":5071100, "ctx":"initandlisten","msg":"Clearing temp directory"}
{"t":{"$date":"2024-10-09T23:16:01.996+05:30"},"s":"I",  "c":"CONTROL",  "id":20536,   "ctx":"initandlisten","msg":"Flow Control is enabled on this deployment"}
```

---

```
 gsaravanan@gs-mac-pro backend % node prisma/seed.js
[
  {
    id: '6706b7f5862492d9ae3ea56b',
    question: 'What is the capital of France?',
    answers: [ 'Paris', 'London', 'Berlin', 'Madrid' ],
    correctAnswer: 'Paris',
    category: 'Geography',
    difficulty: 'Easy'
  }
```

---

```
gsaravanan@gs-mac-pro gpt_demos % mongo
MongoDB shell version v5.0.29
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("b99d23dd-4505-4b4a-8097-b0da5685d585") }
MongoDB server version: 5.0.29
================
Warning: the "mongo" shell has been superseded by "mongosh",
which delivers improved usability and compatibility.The "mongo" shell has been deprecated and will be removed in
an upcoming release.
For installation instructions, see
https://docs.mongodb.com/mongodb-shell/install/
================
---
The server generated these startup warnings when booting: 
        2024-10-09T23:18:43.726+05:30: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
---
rs0:PRIMARY> rs.initiate()
{
        "ok" : 0,
        "errmsg" : "already initialized",
        "code" : 23,
        "codeName" : "AlreadyInitialized",
        "$clusterTime" : {
                "clusterTime" : Timestamp(1728496153, 1),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        },
        "operationTime" : Timestamp(1728496153, 1)
}
rs0:PRIMARY> rs.status()
{
        "set" : "rs0",
        "date" : ISODate("2024-10-09T17:49:23.540Z"),
        "myState" : 1,
        "term" : NumberLong(3),
        "syncSourceHost" : "",
        "syncSourceId" : -1,
        "heartbeatIntervalMillis" : NumberLong(2000),
        "majorityVoteCount" : 1,
        "writeMajorityCount" : 1,
        "votingMembersCount" : 1,
        "writableVotingMembersCount" : 1,
        "optimes" : {
                "lastCommittedOpTime" : {
                        "ts" : Timestamp(1728496153, 1),
                        "t" : NumberLong(3)
                },
                "lastCommittedWallTime" : ISODate("2024-10-09T17:49:13.814Z"),
                "readConcernMajorityOpTime" : {
                        "ts" : Timestamp(1728496153, 1),
                        "t" : NumberLong(3)
                },
                "appliedOpTime" : {
                        "ts" : Timestamp(1728496153, 1),
                        "t" : NumberLong(3)
                },
                "durableOpTime" : {
                        "ts" : Timestamp(1728496153, 1),
                        "t" : NumberLong(3)
                },
                "lastAppliedWallTime" : ISODate("2024-10-09T17:49:13.814Z"),
                "lastDurableWallTime" : ISODate("2024-10-09T17:49:13.814Z")
        },
        "lastStableRecoveryTimestamp" : Timestamp(1728495962, 2),
        "electionCandidateMetrics" : {
                "lastElectionReason" : "electionTimeout",
                "lastElectionDate" : ISODate("2024-10-09T17:48:43.786Z"),
                "electionTerm" : NumberLong(3),
                "lastCommittedOpTimeAtElection" : {
                        "ts" : Timestamp(0, 0),
                        "t" : NumberLong(-1)
                },
                "lastSeenOpTimeAtElection" : {
                        "ts" : Timestamp(1728495962, 2),
                        "t" : NumberLong(2)
                },
                "numVotesNeeded" : 1,
                "priorityAtElection" : 1,
                "electionTimeoutMillis" : NumberLong(10000),
                "newTermStartDate" : ISODate("2024-10-09T17:48:43.796Z"),
                "wMajorityWriteAvailabilityDate" : ISODate("2024-10-09T17:48:43.801Z")
        },
        "members" : [
                {
                        "_id" : 0,
                        "name" : "localhost:27017",
                        "health" : 1,
                        "state" : 1,
                        "stateStr" : "PRIMARY",
                        "uptime" : 41,
                        "optime" : {
                                "ts" : Timestamp(1728496153, 1),
                                "t" : NumberLong(3)
                        },
                        "optimeDate" : ISODate("2024-10-09T17:49:13Z"),
                        "lastAppliedWallTime" : ISODate("2024-10-09T17:49:13.814Z"),
                        "lastDurableWallTime" : ISODate("2024-10-09T17:49:13.814Z"),
                        "syncSourceHost" : "",
                        "syncSourceId" : -1,
                        "infoMessage" : "Could not find member to sync from",
                        "electionTime" : Timestamp(1728496123, 1),
                        "electionDate" : ISODate("2024-10-09T17:48:43Z"),
                        "configVersion" : 1,
                        "configTerm" : 3,
                        "self" : true,
                        "lastHeartbeatMessage" : ""
                }
        ],
        "ok" : 1,
        "$clusterTime" : {
                "clusterTime" : Timestamp(1728496153, 1),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        },
        "operationTime" : Timestamp(1728496153, 1)
}
rs0:PRIMARY> show dbs
admin      0.000GB
config     0.000GB
local      0.000GB
quizAppDB  0.000GB
rs0:PRIMARY> 
```