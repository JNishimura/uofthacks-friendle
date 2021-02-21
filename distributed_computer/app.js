#!/usr/bin/env node

const scheduler = 'https://scheduler.distributed.computer';
const admin = require('firebase-admin');
const { data } = require('xdg-basedir');
const serviceAccount = require('GCP_IAM_JSON');
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});
const db = admin.firestore();

async function main() {
  const compute = require('dcp/compute');
  let startTime;

  // CREATE INPUT DATA
  const profiles = await profilesRef.get();
  profileList = [];
  inputData = [];
  batchedData = [];

  profiles.forEach(doc => {
    var data = doc.data();
      temp = {
        userId: doc.id,
        mbtiVec: data.mbti_vec,
        weightedVec: data.weighted_vec
      }

        profileList.push(temp);
  });

    console.log('Pulled Users');

    for(i = 0; i < profileList.length; i++) {
        for(j = i + 1; j < profileList.length; j++) {
            var temp = {
                first_id: profileList[i].userId,
                second_id: profileList[j].userId,
                first: profileList[i].weightedVec,
                second: profileList[j].mbtiVec
            }
            inputData.push(temp)
        }
    }

    console.log('Formed input data of length ' + inputData.length)

    // BATCH DATA
    var temp = [];

    inputData.forEach(data => {
        if (temp.length == 400) {
            batchedData.push(temp);
            temp = [];
        }
        temp.push(data);
    });

    batchedData.push(temp);

    console.log('Split into ' + batchedData.length + ' batches');

    // CREATE JOB
    const job = compute.for(
        batchedData,
        (batch) => {
            result = [];
            batch.forEach(data => {
                a = data.first
                b = data.second
                var numSum = 0
                var denom_aSum = 0
                var denom_bSum = 0
                
                for(i = 0; i < a.length; i++) {
                numSum += a[i] * b[i];
                denom_aSum += a[i] * a[i];
                denom_bSum += b[i] * b[i];
                }
                
                denom = Math.sqrt(denom_aSum) * Math.sqrt(denom_bSum)
                progress();

                temp = {
                    first_id: data.first_id,
                    second_id: data.second_id,
                    sim: numSum/denom
                };

                result.push(temp);
            });
            return result;
        }
    )

  job.on('accepted', (event) => {
    console.log(' - Job accepted by scheduler, waiting for results');
    console.log(` - Job has id ${job.id}`);
    startTime = Date.now();
  });
  job.on('complete', (event) => {
    console.log(
      `Job Finished, total runtime = ${
        Math.round((Date.now() - startTime) / 100) / 10
      }s`,
    );
  });
  job.on('readystatechange', (event) => {
    console.log(`New ready state: ${event}`);
  });
  job.on('status', (event) => {
    console.log('Received status update:', event);
  });
  job.on('console', ({ message }) => {
    console.log('Received console message:', message);
  });
  job.on('result', ({ result, sliceNumber }) => {
    console.log(
      ` - Received result for slice ${sliceNumber} at ${
        Math.round((Date.now() - startTime) / 100) / 10
      }s`,
    );
  });
  job.on('error', (event) => {
    console.error('Received Error:', event);
  });

  job.public.name = 'Events Example - Nodejs';
  job.public.description = 'DCP-Client Example - examples/node/events.js';

  // This is the default behaviour - change if you have multiple bank accounts
  // const wallet = require('dcp/wallet');
  // const ks = await wallet.get(); /* usually loads ~/.dcp/default.keystore */
  // job.setPaymentAccountKeystore(ks);

  //const results = await job.exec(compute.marketValue);
  // OR
  const results = await job.localExec();

  //console.log('Results are: ', results.values());

  // DO STUFF WITH RESULTS
  
    for (const batch of results) {
        for (const data of batch) {
        var docRef1 = db.collection('sim_scores').doc(data.first_id);
        var writeObj = {};
        writeObj[data.second_id] = data.sim;
        const res1 = await docRef1.set(writeObj, {merge: true})
    
        var docRef2 = db.collection('sim_scores').doc(data.second_id);
        writeObj = {};
        writeObj[data.first_id] = data.sim;
        const res2 = await docRef2.set(writeObj, {merge: true})
        }
    }
}

require('dcp-client')
  .init(scheduler)
  .then(main)
  .finally(() => setImmediate(process.exit));