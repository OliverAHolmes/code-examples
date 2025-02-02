import React from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import Chat from './components/Chat';
import Auth from './components/Auth';
import { AuthProvider } from './context/AuthContext';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Container component="main" maxWidth="md">
          <Auth />
          <Chat />
        </Container>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App; 