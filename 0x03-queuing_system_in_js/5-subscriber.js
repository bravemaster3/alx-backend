// subscribing to a channel
import redis from 'redis';

const subscriber = redis.createClient();
subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});
subscriber.on('error', (error) => {
  console.error('Redis client not connected to the server: ', error.message);
});

subscriber.subscribe('holberton school channel');

subscriber.on('message', (channel, message) => {
  if (message === 'KILL_SERVER' && channel === 'holberton school channel') {
    subscriber.unsubscribe('holberton school channel');
    subscriber.quit();
  }
});
