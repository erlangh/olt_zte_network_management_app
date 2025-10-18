import { useState, useEffect } from 'react';
import {
  Table,
  Button,
  Modal,
  Form,
  Input,
  Space,
  Tag,
  message,
  Popconfirm,
  InputNumber,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  SyncOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { oltAPI } from '../services/api';

export default function OLTManagement() {
  const [olts, setOlts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingOlt, setEditingOlt] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchOlts();
  }, []);

  const fetchOlts = async () => {
    setLoading(true);
    try {
      const response = await oltAPI.getAll();
      setOlts(response.data);
    } catch (error) {
      message.error('Failed to fetch OLTs');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingOlt(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (olt) => {
    setEditingOlt(olt);
    form.setFieldsValue(olt);
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await oltAPI.delete(id);
      message.success('OLT deleted successfully');
      fetchOlts();
    } catch (error) {
      message.error('Failed to delete OLT');
    }
  };

  const handleTest = async (id) => {
    try {
      const response = await oltAPI.test(id);
      if (response.data.is_reachable) {
        message.success('OLT is online and reachable');
      } else {
        message.error('OLT is not reachable');
      }
      fetchOlts();
    } catch (error) {
      message.error('Failed to test connection');
    }
  };

  const handleSync = async (id) => {
    try {
      const response = await oltAPI.sync(id);
      message.success(`Synced successfully! Discovered ${response.data.onus_discovered} ONUs`);
      fetchOlts();
    } catch (error) {
      message.error('Failed to sync OLT');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      if (editingOlt) {
        await oltAPI.update(editingOlt.id, values);
        message.success('OLT updated successfully');
      } else {
        await oltAPI.create(values);
        message.success('OLT created successfully');
      }
      setModalVisible(false);
      fetchOlts();
    } catch (error) {
      message.error(editingOlt ? 'Failed to update OLT' : 'Failed to create OLT');
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'IP Address',
      dataIndex: 'ip_address',
      key: 'ip_address',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        const color = status === 'online' ? 'green' : status === 'offline' ? 'red' : 'default';
        const icon = status === 'online' ? <CheckCircleOutlined /> : <CloseCircleOutlined />;
        return (
          <Tag color={color} icon={icon}>
            {status.toUpperCase()}
          </Tag>
        );
      },
    },
    {
      title: 'Model',
      dataIndex: 'model',
      key: 'model',
      render: (text) => text || 'C320',
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
      render: (text) => text || '-',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<CheckCircleOutlined />}
            onClick={() => handleTest(record.id)}
          >
            Test
          </Button>
          <Button
            type="link"
            icon={<SyncOutlined />}
            onClick={() => handleSync(record.id)}
          >
            Sync
          </Button>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure to delete this OLT?"
            onConfirm={() => handleDelete(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <h1>OLT Management</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          Add OLT
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={olts}
        rowKey="id"
        loading={loading}
      />

      <Modal
        title={editingOlt ? 'Edit OLT' : 'Add OLT'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: 'Please input OLT name!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="ip_address"
            label="IP Address"
            rules={[{ required: true, message: 'Please input IP address!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item name="description" label="Description">
            <Input.TextArea rows={3} />
          </Form.Item>

          <Form.Item name="location" label="Location">
            <Input />
          </Form.Item>

          <Form.Item
            name="snmp_community"
            label="SNMP Community"
            initialValue="public"
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="snmp_port"
            label="SNMP Port"
            initialValue={161}
          >
            <InputNumber min={1} max={65535} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item name="telnet_username" label="Telnet Username">
            <Input />
          </Form.Item>

          <Form.Item name="telnet_password" label="Telnet Password">
            <Input.Password />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
