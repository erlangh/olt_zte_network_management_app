import { useState, useEffect } from 'react';
import {
  Table,
  Button,
  Space,
  Tag,
  message,
  Select,
  Card,
  Row,
  Col,
  Statistic,
} from 'antd';
import {
  SyncOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  SignalFilled,
} from '@ant-design/icons';
import { onuAPI, oltAPI } from '../services/api';

export default function ONUManagement() {
  const [onus, setOnus] = useState([]);
  const [olts, setOlts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedOlt, setSelectedOlt] = useState(null);
  const [stats, setStats] = useState({ total: 0, online: 0, offline: 0 });

  useEffect(() => {
    fetchOlts();
    fetchOnus();
  }, []);

  useEffect(() => {
    fetchOnus();
  }, [selectedOlt]);

  const fetchOlts = async () => {
    try {
      const response = await oltAPI.getAll();
      setOlts(response.data);
    } catch (error) {
      message.error('Failed to fetch OLTs');
    }
  };

  const fetchOnus = async () => {
    setLoading(true);
    try {
      const params = selectedOlt ? { olt_id: selectedOlt } : {};
      const response = await onuAPI.getAll(params);
      setOnus(response.data);
      
      // Calculate stats
      const total = response.data.length;
      const online = response.data.filter(onu => onu.status === 'online').length;
      const offline = total - online;
      setStats({ total, online, offline });
    } catch (error) {
      message.error('Failed to fetch ONUs');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async (id) => {
    try {
      await onuAPI.refresh(id);
      message.success('ONU status refreshed');
      fetchOnus();
    } catch (error) {
      message.error('Failed to refresh ONU status');
    }
  };

  const handleDiscover = async () => {
    if (!selectedOlt) {
      message.warning('Please select an OLT first');
      return;
    }
    
    try {
      const response = await onuAPI.discover(selectedOlt);
      message.success(`Discovered ${response.data.onus_discovered} ONUs`);
      fetchOnus();
    } catch (error) {
      message.error('Failed to discover ONUs');
    }
  };

  const getSignalColor = (power) => {
    if (!power) return 'default';
    if (power >= -23) return 'green';
    if (power >= -27) return 'orange';
    return 'red';
  };

  const columns = [
    {
      title: 'Serial Number',
      dataIndex: 'sn',
      key: 'sn',
      fixed: 'left',
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
        <Tag color={status === 'online' ? 'green' : 'red'} icon={
          status === 'online' ? <CheckCircleOutlined /> : <CloseCircleOutlined />
        }>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'RX Power (dBm)',
      dataIndex: 'rx_power',
      key: 'rx_power',
      render: (power) => power ? (
        <Tag color={getSignalColor(power)} icon={<SignalFilled />}>
          {power.toFixed(2)}
        </Tag>
      ) : '-',
    },
    {
      title: 'TX Power (dBm)',
      dataIndex: 'tx_power',
      key: 'tx_power',
      render: (power) => power ? power.toFixed(2) : '-',
    },
    {
      title: 'Distance (m)',
      dataIndex: 'distance',
      key: 'distance',
      render: (distance) => distance || '-',
    },
    {
      title: 'Service Plan',
      dataIndex: 'service_plan',
      key: 'service_plan',
      render: (text) => text || '-',
    },
    {
      title: 'Actions',
      key: 'actions',
      fixed: 'right',
      render: (_, record) => (
        <Button
          type="link"
          icon={<SyncOutlined />}
          onClick={() => handleRefresh(record.id)}
        >
          Refresh
        </Button>
      ),
    },
  ];

  return (
    <div>
      <h1>ONU Management</h1>

      {/* Stats */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic title="Total ONUs" value={stats.total} />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="Online"
              value={stats.online}
              valueStyle={{ color: '#3f8600' }}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="Offline"
              value={stats.offline}
              valueStyle={{ color: '#cf1322' }}
              prefix={<CloseCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Filters */}
      <div style={{ marginBottom: 16, display: 'flex', gap: 16 }}>
        <Select
          placeholder="Select OLT"
          style={{ width: 200 }}
          allowClear
          onChange={setSelectedOlt}
        >
          {olts.map(olt => (
            <Select.Option key={olt.id} value={olt.id}>
              {olt.name}
            </Select.Option>
          ))}
        </Select>
        <Button icon={<SyncOutlined />} onClick={fetchOnus}>
          Refresh
        </Button>
        <Button type="primary" icon={<SyncOutlined />} onClick={handleDiscover}>
          Discover ONUs
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={onus}
        rowKey="id"
        loading={loading}
        scroll={{ x: 1200 }}
      />
    </div>
  );
}
