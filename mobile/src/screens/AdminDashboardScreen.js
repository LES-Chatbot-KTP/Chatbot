/**
 * Admin dashboard screen — overview metrics and navigation to admin sections.
 */
import React, { useState, useCallback } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert, ScrollView } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { getMetricas } from '../services/adminService';

export default function AdminDashboardScreen({ navigation }) {
  const [metricas, setMetricas] = useState(null);

  useFocusEffect(
    useCallback(() => {
      loadMetricas();
    }, [])
  );

  async function loadMetricas() {
    try {
      const data = await getMetricas();
      setMetricas(data);
    } catch {
      Alert.alert('Erro', 'Não foi possível carregar métricas');
    }
  }

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Painel Administrativo</Text>

      {metricas && (
        <View style={styles.metricsGrid}>
          <MetricCard label="Usuários" value={metricas.total_usuarios} />
          <MetricCard label="Conversas" value={metricas.total_conversas} />
          <MetricCard label="Perguntas" value={metricas.total_perguntas} />
          <MetricCard label="Documentos" value={metricas.total_documentos} />
          <MetricCard label="Docs Ativos" value={metricas.total_documentos_ativos} />
          <MetricCard label="Avaliações" value={metricas.total_avaliacoes} />
          <MetricCard
            label="Média Avaliações"
            value={metricas.media_avaliacoes != null ? metricas.media_avaliacoes.toFixed(1) : 'N/A'}
          />
        </View>
      )}

      <View style={styles.menu}>
        <MenuItem title="Gerenciar Documentos" onPress={() => navigation.navigate('AdminDocuments')} />
        <MenuItem title="Gerenciar Usuários" onPress={() => navigation.navigate('AdminUsers')} />
        <MenuItem title="Ver Logs" onPress={() => navigation.navigate('AdminLogs')} />
      </View>
    </ScrollView>
  );
}

function MetricCard({ label, value }) {
  return (
    <View style={styles.metricCard}>
      <Text style={styles.metricValue}>{value}</Text>
      <Text style={styles.metricLabel}>{label}</Text>
    </View>
  );
}

function MenuItem({ title, onPress }) {
  return (
    <TouchableOpacity style={styles.menuItem} onPress={onPress}>
      <Text style={styles.menuItemText}>{title}</Text>
      <Text style={styles.menuArrow}>›</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  title: { fontSize: 22, fontWeight: 'bold', color: '#333', padding: 16, paddingTop: 16 },
  metricsGrid: { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 8 },
  metricCard: {
    backgroundColor: '#fff', borderRadius: 8, padding: 16, margin: 8,
    width: '43%', alignItems: 'center', elevation: 1,
  },
  metricValue: { fontSize: 24, fontWeight: 'bold', color: '#1a73e8' },
  metricLabel: { fontSize: 12, color: '#666', marginTop: 4 },
  menu: { marginTop: 16, paddingHorizontal: 16 },
  menuItem: {
    backgroundColor: '#fff', borderRadius: 8, padding: 16, marginBottom: 8,
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    elevation: 1,
  },
  menuItemText: { fontSize: 16, color: '#333' },
  menuArrow: { fontSize: 24, color: '#999' },
});
