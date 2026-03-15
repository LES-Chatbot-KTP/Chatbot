/**
 * Chat service — conversations, questions, and history.
 */
import api from './api';

export async function createConversa(titulo) {
  const response = await api.post('/conversas/', { titulo });
  return response.data;
}

export async function listConversas() {
  const response = await api.get('/conversas/');
  return response.data;
}

export async function getHistorico(conversaId) {
  const response = await api.get(`/conversas/${conversaId}/historico`);
  return response.data;
}

export async function askQuestion(conversaId, texto) {
  const response = await api.post(`/conversas/${conversaId}/perguntar`, { texto });
  return response.data;
}

export async function createAvaliacao(respostaId, nota, comentario) {
  const response = await api.post('/avaliacoes/', {
    resposta_id: respostaId,
    nota,
    comentario,
  });
  return response.data;
}
