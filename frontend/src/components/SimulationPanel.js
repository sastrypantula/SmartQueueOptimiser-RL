import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Box,
  Typography,
  CircularProgress,
  Alert
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function SimulationPanel({ onSimulationComplete }) {
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState({
    num_counters: 3,
    num_steps: 500,
    num_episodes: 5,
  });
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConfig(prev => ({
      ...prev,
      [name]: parseInt(value)
    }));
  };

  const handleSimulate = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/simulate`, config);
      onSimulationComplete(response.data.results);
    } catch (err) {
      setError('Failed to run simulation: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
        🎮 Run Simulation
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 2, mb: 3 }}>
        <TextField
          label="Number of Counters"
          type="number"
          name="num_counters"
          value={config.num_counters}
          onChange={handleInputChange}
          fullWidth
        />

        <TextField
          label="Steps per Episode"
          type="number"
          name="num_steps"
          value={config.num_steps}
          onChange={handleInputChange}
          fullWidth
        />

        <TextField
          label="Number of Episodes"
          type="number"
          name="num_episodes"
          value={config.num_episodes}
          onChange={handleInputChange}
          fullWidth
        />
      </Box>

      <Button
        variant="contained"
        color="success"
        onClick={handleSimulate}
        disabled={loading}
        fullWidth
        size="large"
      >
        {loading ? <CircularProgress size={24} sx={{ mr: 1 }} /> : '⚡'}
        {loading ? 'Simulating...' : 'Run Simulation'}
      </Button>
    </Paper>
  );
}

export default SimulationPanel;
