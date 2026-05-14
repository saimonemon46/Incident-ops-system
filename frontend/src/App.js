import AppRouter from './app/router';
import { QueryProvider } from './app/providers/QueryProvider';
import { SocketProvider } from './app/providers/SocketProvider';
import { ThemeProvider } from './app/providers/ThemeProvider';
import './styles/globals.css';

function App() {
  return (
    <ThemeProvider>
      <QueryProvider>
        <SocketProvider>
          <AppRouter />
        </SocketProvider>
      </QueryProvider>
    </ThemeProvider>
  );
}

export default App;
