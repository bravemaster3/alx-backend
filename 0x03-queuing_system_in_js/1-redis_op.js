import redis from 'redis';

const client = redis.createClient();
client.on('connect', () => {
  console.log('Redis client connected to the server');
});
client.on('error', (error) => {
  console.error('Redis client not connected to the server: ', error.message);
});

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, value) => {
    if (err) {
      console.error(err);
    } else {
      console.log(value);
    }
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
