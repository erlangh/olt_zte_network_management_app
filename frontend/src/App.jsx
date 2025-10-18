import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, theme } from 'antd';
import useAuthStore from './store/authStore';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import OLTManagement from './pages/OLTManagement';
import ONUManagement from './pages/ONUManagement';
import ODPManagement from './pages/ODPManagement';
import CableRouteVisualization from './pages/CableRouteVisualization';
import Layout from './components/Layout';
import './App.css';

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorPrimary: '#1890ff',
        },
      }}
    >
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="olt" element={<OLTManagement />} />
            <Route path="onu" element={<ONUManagement />} />
            <Route path="odp" element={<ODPManagement />} />
            <Route path="cable-route" element={<CableRouteVisualization />} />
          </Route>
        </Routes>
      </Router>
    </ConfigProvider>
  );
}

export default App;
