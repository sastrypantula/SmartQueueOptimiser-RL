import React, { useEffect, useState } from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function QueueVisualization() {
  const [queueState, setQueueState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQueueState = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/customers`);
        setQueueState(response.data);
      } catch (err) {
        setError('Failed to fetch queue state: ' + (err.response?.data?.detail || err.message));
      } finally {
        setLoading(false);
      }
    };

    fetchQueueState();
    const interval = setInterval(fetchQueueState, 2000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  const { queue, counters, cumulative_waiting_time } = queueState;

  const getPriorityColor = (priority) => {
    if (priority === 3) return '#ff6b6b';
    if (priority === 2) return '#ffd43b';
    return '#51cf66';
  };

  const getPriorityLabel = (priority) => {
    if (priority === 3) return 'Urgent';
    if (priority === 2) return 'High';
    return 'Normal';
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
        👥 Queue Visualization
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6}>
          <Box sx={{
            p: 2,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 2
          }}>
            <Typography variant="body2">Queue Size</Typography>
            <Typography variant="h4">{queue.length}</Typography>
          </Box>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Box sx={{
            p: 2,
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            color: 'white',
            borderRadius: 2
          }}>
            <Typography variant="body2">Cumulative Wait Time</Typography>
            <Typography variant="h4">{cumulative_waiting_time}</Typography>
          </Box>
        </Grid>
      </Grid>

      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
        Counters Status
      </Typography>
      <Grid container spacing={1} sx={{ mb: 3 }}>
        {counters.map((counter, idx) => (
          <Grid item xs={12} sm={6} md={4} key={idx}>
            <Box sx={{
              p: 2,
              background: counter.busy ? '#ffe0e0' : '#e0ffe0',
              border: counter.busy ? '2px solid #ff6b6b' : '2px solid #51cf66',
              borderRadius: 1
            }}>
              <Typography variant="body2">Counter {counter.id + 1}</Typography>
              <Typography variant="h6">
                {counter.busy ? '🟢 Busy' : '🔴 Available'}
              </Typography>
              <Typography variant="caption">
                Service time left: {counter.service_time_left}
              </Typography>
            </Box>
          </Grid>
        ))}
      </Grid>

      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
        Queue Details
      </Typography>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow sx={{ background: '#f5f5f5' }}>
              <TableCell><strong>ID</strong></TableCell>
              <TableCell><strong>Service Time</strong></TableCell>
              <TableCell><strong>Wait Time</strong></TableCell>
              <TableCell><strong>Priority</strong></TableCell>
              <TableCell><strong>Arrival</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {queue.length > 0 ? (
              queue.slice(0, 10).map((customer, idx) => (
                <TableRow key={idx} sx={{ '&:hover': { background: '#f9f9f9' } }}>
                  <TableCell>{customer.id}</TableCell>
                  <TableCell>{customer.service_time} min</TableCell>
                  <TableCell><strong>{customer.wait_time} min</strong></TableCell>
                  <TableCell>
                    <Chip
                      label={getPriorityLabel(customer.priority)}
                      size="small"
                      sx={{
                        background: getPriorityColor(customer.priority),
                        color: 'white'
                      }}
                    />
                  </TableCell>
                  <TableCell>{customer.arrival_time}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  Queue is empty
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default QueueVisualization;
