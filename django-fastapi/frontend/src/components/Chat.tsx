import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Typography, Paper } from '@mui/material';
import { useAuth } from '../context/AuthContext';

// Define interface for Auth Context
interface AuthContextType {
  token: string | null;
}

function Chat(): JSX.Element {
  const { token } = useAuth() as AuthContextType;
  const [messages, setMessages] = useState<string[]>([]);
  const [message, setMessage] = useState<string>('');
  const [connected, setConnected] = useState<boolean>(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {

    if (!token) return;

    wsRef.current = new WebSocket(`ws://127.0.0.1:8001/ws/${token}`);
  
    wsRef.current.onopen = () => {
      console.log("Echo WebSocket Connected");
      setConnected(true);
    };
    wsRef.current.onmessage = (event) => {
      console.log("Message from server:", event.data);
      setMessages((prev) => [...prev, event.data]);
    };
    wsRef.current.onerror = (event) => {
      console.error("WebSocket error observed:", event);
    };
    wsRef.current.onclose = () => {
      console.log("WebSocket Disconnected");
      setConnected(false);
    };
  
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [token]);
  

  const sendMessage = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    if (message.trim() && wsRef.current) {
      wsRef.current.send(message);
      setMessage('');
    }
  };
  if (!token) {
    return <></>;
  }

  return (
    <Box sx={{ mt: 4 }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 2,
          height: '400px',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <Box sx={{ 
          flexGrow: 1, 
          overflowY: 'auto',
          mb: 2,
          display: 'flex',
          flexDirection: 'column',
          gap: 1
        }}>
          {messages.map((msg, index) => (
            <Paper 
              key={index} 
              sx={{ 
                p: 1,
                backgroundColor: '#f5f5f5',
                maxWidth: '80%',
                alignSelf: 'flex-start'
              }}
            >
              <Typography>{msg}</Typography>
            </Paper>
          ))}
        </Box>
        
        <Box
          component="form"
          onSubmit={sendMessage}
          sx={{
            display: 'flex',
            gap: 1
          }}
        >
          <TextField
            fullWidth
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message..."
            disabled={!connected}
            size="small"
          />
          <Button 
            type="submit" 
            variant="contained" 
            disabled={!connected || !message.trim()}
          >
            Send
          </Button>
        </Box>
      </Paper>
      
      <Typography 
        sx={{ 
          mt: 1, 
          color: connected ? 'success.main' : 'error.main' 
        }}
      >
        {connected ? 'Connected' : 'Disconnected'}
      </Typography>
    </Box>
  );
}

export default Chat;