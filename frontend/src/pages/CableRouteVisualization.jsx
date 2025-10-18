import { useState, useEffect } from 'react';
import { Card, message, Spin } from 'antd';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { oltAPI, odpAPI, onuAPI, cableRouteAPI } from '../services/api';

export default function CableRouteVisualization() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNetworkTopology();
  }, []);

  const fetchNetworkTopology = async () => {
    setLoading(true);
    try {
      // Fetch all network elements
      const [oltsRes, odpsRes, onusRes, routesRes] = await Promise.all([
        oltAPI.getAll(),
        odpAPI.getAll(),
        onuAPI.getAll(),
        cableRouteAPI.getAll(),
      ]);

      const olts = oltsRes.data;
      const odps = odpsRes.data;
      const onus = onusRes.data;
      const routes = routesRes.data;

      // Create nodes
      const newNodes = [];
      const newEdges = [];

      // OLT nodes (top level)
      olts.forEach((olt, index) => {
        newNodes.push({
          id: `olt-${olt.id}`,
          type: 'input',
          data: { 
            label: `🖥️ ${olt.name}\n${olt.ip_address}`,
          },
          position: { x: 250 * index, y: 0 },
          style: {
            background: olt.status === 'online' ? '#52c41a' : '#ff4d4f',
            color: 'white',
            border: '2px solid #fff',
            padding: 10,
            borderRadius: 8,
          },
        });
      });

      // ODP nodes (middle level)
      odps.forEach((odp, index) => {
        const nodeId = `odp-${odp.id}`;
        newNodes.push({
          id: nodeId,
          data: { 
            label: `📍 ${odp.name}\n${odp.splitter_ratio}`,
          },
          position: { x: 200 * index, y: 200 },
          style: {
            background: '#1890ff',
            color: 'white',
            border: '2px solid #fff',
            padding: 10,
            borderRadius: 8,
          },
        });

        // Create edge from OLT to ODP
        if (odp.port_id) {
          // Find OLT - simplified, assumes first OLT
          const oltId = olts[0]?.id;
          if (oltId) {
            newEdges.push({
              id: `olt-${oltId}-odp-${odp.id}`,
              source: `olt-${oltId}`,
              target: nodeId,
              type: 'smoothstep',
              animated: true,
              style: { stroke: '#1890ff', strokeWidth: 2 },
            });
          }
        }
      });

      // ONU nodes (bottom level) - limit to first 20 for visualization
      onus.slice(0, 20).forEach((onu, index) => {
        const nodeId = `onu-${onu.id}`;
        newNodes.push({
          id: nodeId,
          type: 'output',
          data: { 
            label: `📡 ${onu.sn}\n${onu.customer_name || 'No Customer'}`,
          },
          position: { x: 150 * index, y: 400 },
          style: {
            background: onu.status === 'online' ? '#52c41a' : '#ff4d4f',
            color: 'white',
            border: '2px solid #fff',
            padding: 10,
            borderRadius: 8,
            fontSize: 10,
          },
        });

        // Create edge from ODP to ONU
        if (onu.odp_id) {
          newEdges.push({
            id: `odp-${onu.odp_id}-onu-${onu.id}`,
            source: `odp-${onu.odp_id}`,
            target: nodeId,
            type: 'smoothstep',
            style: { 
              stroke: onu.status === 'online' ? '#52c41a' : '#ff4d4f',
              strokeWidth: 1 
            },
          });
        }
      });

      setNodes(newNodes);
      setEdges(newEdges);
    } catch (error) {
      message.error('Failed to fetch network topology');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Cable Route Visualization</h1>
      <Card style={{ height: '70vh', marginTop: 16 }}>
        {loading ? (
          <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100%' 
          }}>
            <Spin size="large" tip="Loading network topology..." />
          </div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            fitView
          >
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        )}
      </Card>
    </div>
  );
}
