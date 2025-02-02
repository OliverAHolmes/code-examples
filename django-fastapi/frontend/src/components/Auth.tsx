import React, { useState } from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';
import { useAuth } from '../context/AuthContext';

function Auth(): JSX.Element {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const { login, token, logout } = useAuth();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    await login(username, password);
  };

  if (token) {
    return (
      <Box sx={{ mt: 2 }}>
        <Button variant="contained" color="secondary" onClick={logout}>
          Logout
        </Button>
      </Box>
    );
  }

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        mt: 2,
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
      }}
    >
      <Typography variant="h5">Login</Typography>
      <TextField
        label="Username"
        value={username}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
        required
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
        required
      />
      <Button type="submit" variant="contained">
        Login
      </Button>
    </Box>
  );
}

export default Auth; 