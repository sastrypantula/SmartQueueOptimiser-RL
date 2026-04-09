import React, { useState } from 'react';
import { Container, Box, Typography, AppBar, Toolbar, CssBaseline } from '@mui/material';
import TrainingPanel from './components/TrainingPanel';
import SimulationPanel from './components/SimulationPanel';
import ResultsPanel from './components/ResultsPanel';
import QueueVisualization from './components/QueueVisualization';

function App() {
  const [simulationResults, setSimulationResults] = useState(null);

  const handleSimulationComplete = (results) => {
    setSimulationResults(results);
  };

  return (
    <>
      <CssBaseline />
      <AppBar position="static" sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            🚀 Smart Queue Optimizer
          </Typography>
          <Typography variant="body2">
            RL-based Queue Management System
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ mb: 3 }}>
          <Typography variant="h4" sx={{ mb: 1, fontWeight: 'bold' }}>
            Welcome to Smart Queue Optimizer
          </Typography>
          <Typography color="textSecondary" sx={{ mb: 3 }}>
            Optimize queue management using Reinforcement Learning. Compare RL agents with traditional strategies (FIFO, SJF).
          </Typography>
        </Box>

        <TrainingPanel />
        <SimulationPanel onSimulationComplete={handleSimulationComplete} />

        {simulationResults && <ResultsPanel results={simulationResults} />}

        <QueueVisualization />
      </Container>

      <Box sx={{ background: '#f5f5f5', py: 3, mt: 4, textAlign: 'center' }}>
        <Typography color="textSecondary" variant="body2">
          © 2024 Smart Queue Optimizer | Powered by FastAPI + React + Stable-Baselines3
        </Typography>
      </Box>
    </>
  );
}

export default App;
