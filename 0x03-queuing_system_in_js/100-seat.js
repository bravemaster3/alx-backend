import express from 'express';
import kue from 'kue';
import redis from 'redis';
import { promisify } from 'util';

// Create Redis client
const client = redis.createClient();
const reserveSeatAsync = promisify(client.set).bind(client);
const getCurrentAvailableSeatsAsync = promisify(client.get).bind(client);

// Reserve seats and get current available seats functions
const reserveSeat = async (number) => {
  await reserveSeatAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const seats = await getCurrentAvailableSeatsAsync('available_seats');
  return parseInt(seats, 10);
};

// Initialize variables
let reservationEnabled = true;
const queue = kue.createQueue();

// Create Express server
const app = express();
const PORT = 1245;

// Set initial number of available seats to 50
reserveSeat(50);

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat', {}).save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', 2, async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();

    if (currentSeats > 0) {
      await reserveSeat(currentSeats - 1);
      const newSeats = await getCurrentAvailableSeats();

      if (newSeats === 0) {
        reservationEnabled = false;
      }

      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
