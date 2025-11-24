import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Optional
from datetime import datetime


class VectorStore:
    
    def __init__(self):
        self.dimension = 768
        self.index_path = "./data/faiss_index.bin"
        self.metadata_path = "./data/faiss_metadata.pkl"
        
        os.makedirs("./data", exist_ok=True)
        
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.load_index()
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            self.id_to_idx = {}
    
    def add_memory(
        self,
        memory_id: str,
        text: str,
        embedding: List[float],
        metadata: Dict
    ):
        try:
            vector = np.array([embedding], dtype=np.float32)
            
            self.index.add(vector)
            
            idx = len(self.metadata)
            self.id_to_idx[memory_id] = idx
            self.metadata.append({
                'id': memory_id,
                'text': text,
                **metadata
            })
            
            self.save_index()
        except Exception as e:
            print(f"Error adding memory to vector store: {e}")
    
    def search_similar(
        self,
        query_embedding: List[float],
        user_id: Optional[str] = None,
        character_id: Optional[str] = None,
        n_results: int = 5
    ) -> List[Dict]:
        try:
            if self.index.ntotal == 0:
                return []
            
            query_vector = np.array([query_embedding], dtype=np.float32)
            
            k = min(n_results * 3, self.index.ntotal)
            distances, indices = self.index.search(query_vector, k)
            
            memories = []
            for i, idx in enumerate(indices[0]):
                if idx == -1:
                    continue
                
                meta = self.metadata[idx]
                
                if user_id and meta.get('user_id') != user_id:
                    continue
                if character_id and meta.get('character_id') != character_id:
                    continue
                
                memories.append({
                    'id': meta['id'],
                    'text': meta['text'],
                    'metadata': {k: v for k, v in meta.items() if k not in ['id', 'text']},
                    'distance': float(distances[0][i])
                })
                
                if len(memories) >= n_results:
                    break
            
            return memories
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []
    
    def delete_memory(self, memory_id: str):
        try:
            if memory_id in self.id_to_idx:
                idx = self.id_to_idx[memory_id]
                self.metadata[idx]['deleted'] = True
                self.save_index()
        except Exception as e:
            print(f"Error deleting memory: {e}")
    
    def get_collection_count(self) -> int:
        try:
            return sum(1 for m in self.metadata if not m.get('deleted', False))
        except Exception as e:
            print(f"Error getting collection count: {e}")
            return 0
    
    def save_index(self):
        try:
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, 'wb') as f:
                pickle.dump({
                    'metadata': self.metadata,
                    'id_to_idx': self.id_to_idx
                }, f)
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def load_index(self):
        try:
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                data = pickle.load(f)
                self.metadata = data['metadata']
                self.id_to_idx = data['id_to_idx']
        except Exception as e:
            print(f"Error loading index: {e}")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            self.id_to_idx = {}
    
    def reset_collection(self):
        try:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            self.id_to_idx = {}
            self.save_index()
        except Exception as e:
            print(f"Error resetting collection: {e}")


vector_store = VectorStore()
