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

function TrainingPanel() {
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState({
    algorithm: 'PPO',
    total_timesteps: 50000,
    num_counters: 3,
    learning_rate: 0.0003,
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConfig(prev => ({
      ...prev,
      [name]: name === 'algorithm' ? value : (
        name === 'total_timesteps' || name === 'num_counters' 
          ? parseInt(value) 
          : parseFloat(value)
      )
    }));
  };

  const handleTrain = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/train`, config);
      setResult(response.data);
    } catch (err) {
      setError('Failed to train model: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
        🤖 RL Agent Training
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {result && <Alert severity="success" sx={{ mb: 2 }}>{result.message}</Alert>}

      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 3 }}>
        <TextField
          label="Algorithm"
          select
          SelectProps={{ native: true }}
          name="algorithm"
          value={config.algorithm}
          onChange={handleInputChange}
          fullWidth
        >
          <option value="PPO">PPO</option>
          <option value="DQN">DQN</option>
        </TextField>

        <TextField
          label="Number of Counters"
          type="number"
          name="num_counters"
          value={config.num_counters}
          onChange={handleInputChange}
          fullWidth
        />

        <TextField
          label="Total Timesteps"
          type="number"
          name="total_timesteps"
          value={config.total_timesteps}
          onChange={handleInputChange}
          fullWidth
        />

        <TextField
          label="Learning Rate"
          type="number"
          name="learning_rate"
          value={config.learning_rate}
          onChange={handleInputChange}
          inputProps={{ step: '0.0001' }}
          fullWidth
        />
      </Box>

      <Button
        variant="contained"
        color="primary"
        onClick={handleTrain}
        disabled={loading}
        fullWidth
        size="large"
      >
        {loading ? <CircularProgress size={24} sx={{ mr: 1 }} /> : '▶'}
        {loading ? 'Training...' : 'Start Training'}
      </Button>
    </Paper>
  );
}

export default TrainingPanel;
