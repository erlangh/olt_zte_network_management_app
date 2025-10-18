import { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Table, Tag, Alert } from 'antd';
import {
  CloudServerOutlined,
  ApiOutlined,
  NodeIndexOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import { dashboardAPI } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [recentOnus, setRecentOnus] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, onusRes, alertsRes] = await Promise.all([
        dashboardAPI.getStats(),
        dashboardAPI.getRecentOnus(),
        dashboardAPI.getAlerts(),
      ]);
      setStats(statsRes.data);
      setRecentOnus(onusRes.data);
      setAlerts(alertsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const onuColumns = [
    {
      title: 'Serial Number',
      dataIndex: 'sn',
      key: 'sn',
    },
    {
      title: 'Customer',
      dataIndex: 'customer_name',
      key: 'customer_name',
      render: (text) => text || '-',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'online' ? 'green' : 'red'}>
          {status === 'online' ? <CheckCircleOutlined /> : <CloseCircleOutlined />}{' '}
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Created At',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => new Date(date).toLocaleString(),
    },
  ];

  return (
    <div>
      <h1>Dashboard</h1>

      {/* Stats Cards */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="OLT Devices"
              value={stats?.olts.total || 0}
              prefix={<CloudServerOutlined />}
              suffix={`/ ${stats?.olts.online || 0} Online`}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total ONUs"
              value={stats?.onus.total || 0}
              prefix={<ApiOutlined />}
              valueStyle={{
                color: stats?.onus.online > 0 ? '#3f8600' : undefined,
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Online ONUs"
              value={stats?.onus.online || 0}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="ODPs"
              value={stats?.odps.total || 0}
              prefix={<NodeIndexOutlined />}
              suffix={`/ ${stats?.odps.active || 0} Active`}
            />
          </Card>
        </Col>
      </Row>

      {/* Port Utilization */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={24}>
          <Card>
            <Statistic
              title="Port Utilization"
              value={stats?.port_utilization || 0}
              suffix="%"
              precision={2}
              valueStyle={{
                color: (stats?.port_utilization || 0) > 80 ? '#cf1322' : '#3f8600',
              }}
            />
          </Card>
        </Col>
      </Row>

      {/* Alerts */}
      {alerts.length > 0 && (
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col span={24}>
            <Card title={<><WarningOutlined /> Alerts</>}>
              {alerts.map((alert, index) => (
                <Alert
                  key={index}
                  message={alert.title}
                  description={alert.message}
                  type={alert.type}
                  showIcon
                  style={{ marginBottom: 8 }}
                />
              ))}
            </Card>
          </Col>
        </Row>
      )}

      {/* Recent ONUs */}
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card title="Recent ONUs">
            <Table
              columns={onuColumns}
              dataSource={recentOnus}
              rowKey="id"
              loading={loading}
              pagination={{ pageSize: 5 }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}
