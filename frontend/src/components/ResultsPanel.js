import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  Card,
  CardContent
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

function ResultsPanel({ results }) {
  if (!results) {
    return null;
  }

  const { rl, fifo, sjf, improvements } = results;

  // Prepare data for comparison chart
  const comparisonData = [
    {
      name: 'RL',
      'Avg Wait Time': rl.avg_wait_time.toFixed(2),
      'Customers Served': rl.avg_customers_served.toFixed(0)
    },
    {
      name: 'FIFO',
      'Avg Wait Time': fifo.avg_wait_time.toFixed(2),
      'Customers Served': fifo.avg_customers_served.toFixed(0)
    },
    {
      name: 'SJF',
      'Avg Wait Time': sjf.avg_wait_time.toFixed(2),
      'Customers Served': sjf.avg_customers_served.toFixed(0)
    }
  ];

  // Prepare episode data
  const rlEpisodes = rl.wait_times.map((wt, idx) => ({
    episode: idx + 1,
    'RL': wt.toFixed(2),
    'FIFO': fifo.wait_times[idx].toFixed(2),
    'SJF': sjf.wait_times[idx].toFixed(2)
  }));

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        📊 Simulation Results
      </Typography>

      {/* Improvements Summary */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6}>
          <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
            <CardContent>
              <Typography color="white" variable="subtitle2">
                RL vs FIFO Improvement
              </Typography>
              <Typography color="white" variant="h4" sx={{ mt: 1 }}>
                {improvements.rl_vs_fifo}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
            <CardContent>
              <Typography color="white" variable="subtitle2">
                RL vs SJF Improvement
              </Typography>
              <Typography color="white" variant="h4" sx={{ mt: 1 }}>
                {improvements.rl_vs_sjf}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Metrics Table */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        {[
          { title: 'RL Strategy', data: rl, color: '#667eea' },
          { title: 'FIFO Strategy', data: fifo, color: '#764ba2' },
          { title: 'SJF Strategy', data: sjf, color: '#f093fb' }
        ].map((item, idx) => (
          <Grid item xs={12} sm={6} md={4} key={idx}>
            <Card sx={{ borderTop: `4px solid ${item.color}` }}>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  {item.title}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2">
                    <strong>Avg Wait Time:</strong> {item.data.avg_wait_time.toFixed(2)}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Std Dev:</strong> {item.data.std_wait_time.toFixed(2)}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Customers Served:</strong> {item.data.avg_customers_served.toFixed(0)}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Average Wait Time Comparison */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
          Average Wait Times Comparison
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={comparisonData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Avg Wait Time" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </Box>

      {/* Episode-by-Episode Wait Times */}
      <Box>
        <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
          Wait Time Trends Across Episodes
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={rlEpisodes}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="episode" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="RL" stroke="#667eea" strokeWidth={2} />
            <Line type="monotone" dataKey="FIFO" stroke="#764ba2" strokeWidth={2} />
            <Line type="monotone" dataKey="SJF" stroke="#f093fb" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
}

export default ResultsPanel;
