/**
 * Admin documents screen — list, create, and manage documents.
 */
import React, { useState, useCallback } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, TextInput, StyleSheet, Alert, Modal,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { listDocumentos, createDocumento, reindexDocumento } from '../services/adminService';

export default function AdminDocumentsScreen() {
  const [documentos, setDocumentos] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [titulo, setTitulo] = useState('');
  const [conteudo, setConteudo] = useState('');

  useFocusEffect(
    useCallback(() => {
      loadDocumentos();
    }, [])
  );

  async function loadDocumentos() {
    try {
      const data = await listDocumentos();
      setDocumentos(data);
    } catch {
      Alert.alert('Erro', 'Não foi possível carregar documentos');
    }
  }

  async function handleCreate() {
    if (!titulo || !conteudo) {
      Alert.alert('Erro', 'Preencha todos os campos');
      return;
    }
    try {
      await createDocumento({ titulo, conteudo });
      setTitulo('');
      setConteudo('');
      setModalVisible(false);
      loadDocumentos();
      Alert.alert('Sucesso', 'Documento criado');
    } catch {
      Alert.alert('Erro', 'Não foi possível criar documento');
    }
  }

  async function handleReindex(id) {
    try {
      const job = await reindexDocumento(id);
      Alert.alert('Indexação', `Status: ${job.status}`);
    } catch {
      Alert.alert('Erro', 'Não foi possível reindexar');
    }
  }

  function renderItem({ item }) {
    return (
      <View style={styles.card}>
        <Text style={styles.cardTitle}>{item.titulo}</Text>
        <Text style={styles.cardStatus}>{item.ativo ? 'Ativo' : 'Inativo'}</Text>
        <TouchableOpacity style={styles.reindexButton} onPress={() => handleReindex(item.id)}>
          <Text style={styles.reindexText}>Reindexar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={documentos}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderItem}
        ListEmptyComponent={<Text style={styles.empty}>Nenhum documento</Text>}
      />

      <TouchableOpacity style={styles.fab} onPress={() => setModalVisible(true)}>
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>

      <Modal visible={modalVisible} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Novo Documento</Text>
            <TextInput
              style={styles.input}
              placeholder="Título"
              value={titulo}
              onChangeText={setTitulo}
            />
            <TextInput
              style={[styles.input, styles.textArea]}
              placeholder="Conteúdo"
              value={conteudo}
              onChangeText={setConteudo}
              multiline
              numberOfLines={6}
            />
            <TouchableOpacity style={styles.saveButton} onPress={handleCreate}>
              <Text style={styles.saveText}>Salvar</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setModalVisible(false)}>
              <Text style={styles.cancelText}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  card: {
    backgroundColor: '#fff', marginHorizontal: 16, marginVertical: 6,
    padding: 16, borderRadius: 8, elevation: 1,
  },
  cardTitle: { fontSize: 16, fontWeight: '500', color: '#333' },
  cardStatus: { fontSize: 12, color: '#666', marginTop: 4 },
  reindexButton: { marginTop: 8, alignSelf: 'flex-start' },
  reindexText: { color: '#1a73e8', fontWeight: '500' },
  empty: { textAlign: 'center', color: '#999', marginTop: 40 },
  fab: {
    position: 'absolute', right: 24, bottom: 24,
    width: 56, height: 56, borderRadius: 28,
    backgroundColor: '#1a73e8', justifyContent: 'center', alignItems: 'center',
    elevation: 4,
  },
  fabText: { color: '#fff', fontSize: 28, lineHeight: 28 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center' },
  modalContent: { backgroundColor: '#fff', marginHorizontal: 24, borderRadius: 12, padding: 24 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 16 },
  input: {
    borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12,
    marginBottom: 12, fontSize: 15,
  },
  textArea: { height: 120, textAlignVertical: 'top' },
  saveButton: { backgroundColor: '#1a73e8', borderRadius: 8, padding: 14, alignItems: 'center' },
  saveText: { color: '#fff', fontWeight: '600', fontSize: 16 },
  cancelText: { color: '#e53935', textAlign: 'center', marginTop: 12, fontSize: 15 },
});
