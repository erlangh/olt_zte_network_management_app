import { useState, useEffect } from 'react';
import {
  Table,
  Button,
  Modal,
  Form,
  Input,
  Space,
  message,
  Popconfirm,
  InputNumber,
  Select,
  Tag,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EnvironmentOutlined,
} from '@ant-design/icons';
import { odpAPI } from '../services/api';

export default function ODPManagement() {
  const [odps, setOdps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingOdp, setEditingOdp] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchOdps();
  }, []);

  const fetchOdps = async () => {
    setLoading(true);
    try {
      const response = await odpAPI.getAll();
      setOdps(response.data);
    } catch (error) {
      message.error('Failed to fetch ODPs');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingOdp(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (odp) => {
    setEditingOdp(odp);
    form.setFieldsValue(odp);
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      await odpAPI.delete(id);
      message.success('ODP deleted successfully');
      fetchOdps();
    } catch (error) {
      message.error('Failed to delete ODP');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      if (editingOdp) {
        await odpAPI.update(editingOdp.id, values);
        message.success('ODP updated successfully');
      } else {
        await odpAPI.create(values);
        message.success('ODP created successfully');
      }
      setModalVisible(false);
      fetchOdps();
    } catch (error) {
      message.error(editingOdp ? 'Failed to update ODP' : 'Failed to create ODP');
    }
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Code',
      dataIndex: 'code',
      key: 'code',
      render: (text) => text || '-',
    },
    {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
      render: (text) => text || '-',
    },
    {
      title: 'Splitter',
      dataIndex: 'splitter_ratio',
      key: 'splitter_ratio',
      render: (text) => <Tag>{text}</Tag>,
    },
    {
      title: 'Ports',
      key: 'ports',
      render: (_, record) => (
        <span>
          {record.used_ports} / {record.total_ports} used
        </span>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'active' ? 'green' : 'default'}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Location',
      key: 'location',
      render: (_, record) => (
        record.latitude && record.longitude ? (
          <Button
            type="link"
            icon={<EnvironmentOutlined />}
            onClick={() => window.open(
              `https://www.google.com/maps?q=${record.latitude},${record.longitude}`,
              '_blank'
            )}
          >
            View Map
          </Button>
        ) : '-'
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure to delete this ODP?"
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
        <h1>ODP Management</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          Add ODP
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={odps}
        rowKey="id"
        loading={loading}
      />

      <Modal
        title={editingOdp ? 'Edit ODP' : 'Add ODP'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: 'Please input ODP name!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item name="code" label="Code">
            <Input />
          </Form.Item>

          <Form.Item name="address" label="Address">
            <Input.TextArea rows={2} />
          </Form.Item>

          <Form.Item
            name="splitter_ratio"
            label="Splitter Ratio"
            initialValue="1:8"
          >
            <Select>
              <Select.Option value="1:2">1:2</Select.Option>
              <Select.Option value="1:4">1:4</Select.Option>
              <Select.Option value="1:8">1:8</Select.Option>
              <Select.Option value="1:16">1:16</Select.Option>
              <Select.Option value="1:32">1:32</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="total_ports"
            label="Total Ports"
            initialValue={8}
          >
            <InputNumber min={1} max={128} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item name="latitude" label="Latitude">
            <InputNumber
              style={{ width: '100%' }}
              placeholder="-90 to 90"
              min={-90}
              max={90}
              step={0.000001}
            />
          </Form.Item>

          <Form.Item name="longitude" label="Longitude">
            <InputNumber
              style={{ width: '100%' }}
              placeholder="-180 to 180"
              min={-180}
              max={180}
              step={0.000001}
            />
          </Form.Item>

          <Form.Item name="description" label="Description">
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
