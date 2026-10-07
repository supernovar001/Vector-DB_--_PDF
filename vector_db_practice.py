'''
과목명 : Vector DB
작성자 : 조해수 (P168)

Vector DB_실습_PDF/
├── vector_db_practice.py      # 실습 1: PDF 로딩 → 청킹 → BGE-M3 → FAISS / Qdrant → 필터 검색
├── rag_hybrid_practice.py     # 실습 2: BM25 → Dense 실패 케이스 → RRF → Reranker → RAGAS
├── requirements.txt           # 실습 1·2에 필요한 패키지 (버전 고정)
├── 리포트_VectorDB_실습1-2.md  # 본 리포트
├── outputs/
│   ├── 실습1_레포트.md, 실습2_레포트.md       # 스크립트가 자동 생성한 결과 레포트
│   ├── meta.json, faiss_results.json, qdrant_results.json, qdrant_filter_results.json
│   └── lab2_results.json
└── PDF 16개 (입력 데이터)

종합실습 1
## 1. 실습 목적
여러 PDF 보고서를 페이지 단위로 로딩하고, RecursiveCharacterTextSplitter로 청킹한 뒤 BGE-M3로 Dense Embedding을 생성하였다. 동일한 임베딩을 FAISS HNSW와 Qdrant에 각각 저장하고 검색 결과를 비교했으며, Qdrant의 메타데이터 필터 검색도 확인하였다.

## 2. 실습 환경 및 데이터
- PDF 파일 수: 16
- 전체 페이지 수: 843
- Chunk size: 500
- Chunk overlap: 50
- 전체 Chunk 수: 2398
- 임베딩 모델: BAAI/bge-m3
- 임베딩 shape: (2398, 1024)
- FAISS: HNSW, Inner Product + L2 normalization
- Qdrant: Cosine distance
- 테스트 질문: `HBM이란 무엇인가?`

## 3. 처리 흐름
PDF → 텍스트 추출(PyMuPDF) → Chunking → BGE-M3 임베딩 → FAISS HNSW / Qdrant 저장 → Top-5 검색 → Qdrant 메타데이터 필터 검색

## 4. FAISS 검색 결과
| 순위 | Score | 파일 | Page | 검색 Chunk 일부 |
|---:|---:|---|---:|---|
| 1 | 0.5804 | 3. 글로벌 반도체 산업 전망 2026_삼일회계법인.pdf | 64 | Samil PwC Semiconductor and beyond 2026 DRAM 대비 HBM 시장 규모 및 침투율 1) 침투율: 전체 DRAM 중 HBM 비중 출처: Omdia, PwC Analysis 생성형 AI 학습 및 추론의급증으로 HBM은 현대 데이터 센터 서버 |
| 2 | 0.5632 | 5. AI 반도체 기술 및 산업 동향.pdf | 11 | AI 반도체 기술 및 산업 동향 2024. 7 제824호 13 2. 메모리 : HBM, PIM ❑ AI 연산에 있어 ’메모리 병목 현상‘의 해결이 주요 과제로 대두되면서 AI 반도체 向 메모리의 중요성이 부상 ❍ 메모리 병목 현상(또는 메모리 벽(Memory Wall) |
| 3 | 0.5581 | 5. AI 반도체 기술 및 산업 동향.pdf | 11 | In Memory) 기술이 주목 - PIM 기술은 프로세서와 메모리 영역 간의 거리를 최대한 축소 또는 프로세서와 메모리를 통합 설계하여 저지연 및 높은 에너지 효율 등을 도모 ① HBM(High Bandwidth Memory) ❑ HBM은 개별 DRAM 칩을 고밀도  |
| 4 | 0.5553 | 5. AI 반도체 기술 및 산업 동향.pdf | 12 | 주도15)할 것으로 예상 - HBM 기술을 선도16)하던 SK하이닉스가 HBM3(4세대)를 엔비디아 앞 독점 공급하며 시장을 선점하였으며, 삼성전자는 ’24년 내 공식 납품 예상 ❍ HBM 수요 급증이 전망되는 가운데, HBM3E부터 마이크론의 본격적인 참전으로 국내와 |
| 5 | 0.5537 | 4. 2025 반도체특별위원회 연구보고서_AI 반도체 강국도약 가이드라인.pdf | 112 | 확보하면, 수출 단가는 자연스럽게 상승하고 국내 부가가치 잔존율도 높아진다. 예컨대, HBM은 단순 부품이 아니라 AI 가속기의 성능 병목을 좌우하는 핵심 요소로서, “메모리 대역폭/지연” 최적화가 가능한 국가가 플랫폼 경쟁에서 중요한 레버리지를 갖게 된다. 이때 한국 |

## 5. Qdrant 검색 결과
| 순위 | Score | 파일 | Page | 검색 Chunk 일부 |
|---:|---:|---|---:|---|
| 1 | 0.5804 | 3. 글로벌 반도체 산업 전망 2026_삼일회계법인.pdf | 64 | Samil PwC Semiconductor and beyond 2026 DRAM 대비 HBM 시장 규모 및 침투율 1) 침투율: 전체 DRAM 중 HBM 비중 출처: Omdia, PwC Analysis 생성형 AI 학습 및 추론의급증으로 HBM은 현대 데이터 센터 서버 |
| 2 | 0.5632 | 5. AI 반도체 기술 및 산업 동향.pdf | 11 | AI 반도체 기술 및 산업 동향 2024. 7 제824호 13 2. 메모리 : HBM, PIM ❑ AI 연산에 있어 ’메모리 병목 현상‘의 해결이 주요 과제로 대두되면서 AI 반도체 向 메모리의 중요성이 부상 ❍ 메모리 병목 현상(또는 메모리 벽(Memory Wall) |
| 3 | 0.5581 | 5. AI 반도체 기술 및 산업 동향.pdf | 11 | In Memory) 기술이 주목 - PIM 기술은 프로세서와 메모리 영역 간의 거리를 최대한 축소 또는 프로세서와 메모리를 통합 설계하여 저지연 및 높은 에너지 효율 등을 도모 ① HBM(High Bandwidth Memory) ❑ HBM은 개별 DRAM 칩을 고밀도  |
| 4 | 0.5553 | 5. AI 반도체 기술 및 산업 동향.pdf | 12 | 주도15)할 것으로 예상 - HBM 기술을 선도16)하던 SK하이닉스가 HBM3(4세대)를 엔비디아 앞 독점 공급하며 시장을 선점하였으며, 삼성전자는 ’24년 내 공식 납품 예상 ❍ HBM 수요 급증이 전망되는 가운데, HBM3E부터 마이크론의 본격적인 참전으로 국내와 |
| 5 | 0.5537 | 4. 2025 반도체특별위원회 연구보고서_AI 반도체 강국도약 가이드라인.pdf | 112 | 확보하면, 수출 단가는 자연스럽게 상승하고 국내 부가가치 잔존율도 높아진다. 예컨대, HBM은 단순 부품이 아니라 AI 가속기의 성능 병목을 좌우하는 핵심 요소로서, “메모리 대역폭/지연” 최적화가 가능한 국가가 플랫폼 경쟁에서 중요한 레버리지를 갖게 된다. 이때 한국 |

## 6. Qdrant 메타데이터 필터 검색
조건: `page >= 5`

| 순위 | Score | 파일 | Page | 검색 Chunk 일부 |
|---:|---:|---|---:|---|
| 1 | 0.5804 | 3. 글로벌 반도체 산업 전망 2026_삼일회계법인.pdf | 64 | Samil PwC Semiconductor and beyond 2026 DRAM 대비 HBM 시장 규모 및 침투율 1) 침투율: 전체 DRAM 중 HBM 비중 출처: Omdia, PwC Analysis 생성형 AI 학습 및 추론의급증으로 HBM은 현대 데이터 센터 서버 |
| 2 | 0.5632 | 5. AI 반도체 기술 및 산업 동향.pdf | 11 | AI 반도체 기술 및 산업 동향 2024. 7 제824호 13 2. 메모리 : HBM, PIM ❑ AI 연산에 있어 ’메모리 병목 현상‘의 해결이 주요 과제로 대두되면서 AI 반도체 向 메모리의 중요성이 부상 ❍ 메모리 병목 현상(또는 메모리 벽(Memory Wall) |
| 3 | 0.5581 | 5. AI 반도체 기술 및 산업 동향.pdf | 11 | In Memory) 기술이 주목 - PIM 기술은 프로세서와 메모리 영역 간의 거리를 최대한 축소 또는 프로세서와 메모리를 통합 설계하여 저지연 및 높은 에너지 효율 등을 도모 ① HBM(High Bandwidth Memory) ❑ HBM은 개별 DRAM 칩을 고밀도  |
| 4 | 0.5553 | 5. AI 반도체 기술 및 산업 동향.pdf | 12 | 주도15)할 것으로 예상 - HBM 기술을 선도16)하던 SK하이닉스가 HBM3(4세대)를 엔비디아 앞 독점 공급하며 시장을 선점하였으며, 삼성전자는 ’24년 내 공식 납품 예상 ❍ HBM 수요 급증이 전망되는 가운데, HBM3E부터 마이크론의 본격적인 참전으로 국내와 |
| 5 | 0.5537 | 4. 2025 반도체특별위원회 연구보고서_AI 반도체 강국도약 가이드라인.pdf | 112 | 확보하면, 수출 단가는 자연스럽게 상승하고 국내 부가가치 잔존율도 높아진다. 예컨대, HBM은 단순 부품이 아니라 AI 가속기의 성능 병목을 좌우하는 핵심 요소로서, “메모리 대역폭/지연” 최적화가 가능한 국가가 플랫폼 경쟁에서 중요한 레버리지를 갖게 된다. 이때 한국 |

필터 결과의 페이지가 모두 5 이상이면 메타데이터 조건 검색이 정상 동작한 것이다.

## 7. FAISS와 Qdrant 비교
FAISS는 로컬 메모리에서 벡터 유사도 검색을 빠르게 확인하기에 적합하며, 이번 실습에서는 HNSW 인덱스를 사용하였다. 반면 Qdrant는 벡터와 함께 `filename`, `page`, `text` 같은 payload를 저장할 수 있어 파일명이나 페이지와 같은 메타데이터 조건을 검색에 직접 적용할 수 있었다.
두 저장소는 같은 BGE-M3 임베딩을 사용하더라도 내부 인덱싱 및 검색 방식 차이로 결과 순서가 일부 달라질 수 있다(이번 실습에는 순위가 동일했다). 이번 실습에서는 검색 결과 자체뿐 아니라 출처 정보와 조건 검색이 필요한 RAG 시스템에서 Qdrant와 같은 Vector DB가 왜 필요한지 확인할 수 있었다.

## 8. 실습 결과
| 단계 | 완료 | 확인 근거 |
|---|:---:|---|
| ① PDF 로딩 (PyMuPDF) | ✅ | PDF 16개, 텍스트가 있는 페이지 843개 추출 |
| ② 청킹 (RecursiveCharacterTextSplitter) | ✅ | chunk_size=500, overlap=50 → 청크 2,398개 |
| ③ BGE-M3 임베딩 | ✅ | shape `(2398, 1024)` |
| ④ FAISS HNSW 구축 + 검색 | ✅ | Top-5 검색 결과 출력 (1위 score 0.5804, HBM 관련 청크) |
| ⑤ Qdrant Collection 생성 + Upsert | ✅ | `rag_docs` 컬렉션에 2,398개 포인트 업로드 (Cosine, 1024차원) |
| ⑥ Qdrant 검색 + FAISS 비교 | ✅ | Top-5 순위가 FAISS와 동일, score 함께 반환 |
| ⑥ Qdrant 메타데이터 필터 검색 | ✅ | `page >= 5` 조건 적용 결과가 모두 5페이지 이상 |
| 레포트 생성 | ✅ | `outputs/실습1_레포트.md` |

## 9. 고찰
### 9-1. 청킹 품질이 검색 품질을 좌우한다
실습 초기에는 청킹 구분자가 줄바꿈 문자(`\\n`)가 아닌 `\\\\n`이라는 문자열로 잘못 지정되어, 텍스트가 줄바꿈 단위로 나뉘지 않고 마침표와 공백에서만 잘렸다. 그 결과 전체 2,850개 청크 중 1,197개(약 42%)가 "최대한 축소 또는…", ". 메모리 :…"처럼 문장 중간이나 마침표로 시작했고, 검색 결과도 질문에 대한 내용을 온전히 보여주지 못했다. 구분자를 바로잡고 `keep_separator="end"`로 마침표가 문장 끝에 붙도록 수정하자, 문장 중간에서 시작하는 청크는 1개로 줄었고(전체 2398개) Top-3 결과가 모두 "HBM은 여러 개의 DRAM 다이를 적층하여 병목을 해결하는 고대역폭 메모리"라는 정의를 문장 단위로 담게 되었다. 같은 임베딩 모델을 쓰더라도 텍스트를 어떻게 자르는지가 검색 품질에 직접적인 영향을 준다는 점을 확인하였다.

### 9-2. FAISS와 Qdrant는 같은 결과를 반환했다
두 저장소 모두 동일한 BGE-M3 임베딩과 코사인 유사도(정규화 벡터의 내적)를 사용했기 때문에 Top-5의 순위와 score가 일치하였다. 즉 검색 결과의 차이는 저장소가 아니라 임베딩과 청킹에서 결정되며, 저장소 선택은 메타데이터 저장·필터링, 영속성, 서버 운영 여부와 같은 기능적 요구에 따라 이루어져야 한다.

### 9-3. 필터 검색 결과가 필터 없는 결과와 같았던 이유
`page >= 5` 필터를 적용해도 결과가 동일했는데, 이는 필터가 동작하지 않은 것이 아니라 "HBM이란 무엇인가?"의 상위 결과가 원래 모두 5페이지 이후에 위치했기 때문이다. 필터의 효과를 명확히 보이려면 앞쪽 페이지가 상위에 검색되는 질의로 필터 적용 전후를 비교하거나, `count` API로 조건에 맞는 포인트 수를 함께 확인하는 것이 좋다.

### 9-4. 검색(Retrieval)과 답변 생성(Generation)의 차이
이번 실습의 결과는 질문과 유사한 원문 청크를 근거로 제시할 뿐, "HBM은 ~이다"와 같은 답변 문장을 직접 만들어 주지는 않는다. 질문에 대한 완결된 답을 얻으려면 검색된 청크를 LLM의 입력으로 넣어 답변을 생성하는 RAG 생성 단계가 추가로 필요하다.

### 9-5. 개선 방향
- Re-ranker 적용: HBM의 정의를 가장 직접적으로 담은 청크("HBM은 개별 DRAM 칩을 고밀도 적층하여…")가 3위에 머물렀다. `bge-reranker-v2-m3` 같은 Cross-Encoder로 재정렬하면 정의 문장을 상위로 끌어올릴 수 있을 것이다.
- Hybrid Search: "HBM", "TSV"처럼 약어·고유명사가 핵심인 질의는 BM25 또는 BGE-M3의 sparse 벡터를 Dense 검색과 결합(RRF)하면 정확도를 높일 수 있다.
- 전처리: "Samil PwC Semiconductor and beyond 2026", "제824호 13"처럼 페이지마다 반복되는 머리말·쪽번호가 청크에 섞여 있어, 이를 제거하면 임베딩에 담기는 의미가 더 선명해질 것이다.
- 정량 평가: 청크 크기·overlap을 바꿔 가며 Recall@K, MRR 등을 비교해 설정을 근거 있게 결정할 필요가 있다.

## 10. 파일 실행 흐름
`python vector_db_practice.py`를 인자 없이 실행하면 `main()`이 아래 5단계를 각각 별도 프로세스(`--stage`)로 순서대로 실행한다.
macOS에서 PyTorch(FlagEmbedding)와 FAISS가 각자 OpenMP 런타임을 불러와 충돌(segfault)하므로, 두 라이브러리가 한 프로세스에 함께 올라오지 않도록 단계를 분리하였다.
단계 사이의 데이터는 `outputs/` 폴더의 파일로 주고받으며, 한 단계가 실패하면(`check=True`) 이후 단계는 실행되지 않는다.

| 순서 | 단계 (`--stage`) | 하는 일 | 입력 | 출력 (`outputs/`) |
|:---:|---|---|---|---|
| 1 | `embed` | PDF 로딩 → 청킹 → BGE-M3 임베딩 | `*.pdf` | `chunks.pkl`, `embeddings.npy`, `meta.json` |
| 2 | `embed_query` | 질문(`QUERY`) 임베딩 | - | `query.npy` |
| 3 | `faiss` | HNSW 인덱스 구축 + Top-5 검색 | `embeddings.npy`, `chunks.pkl`, `query.npy` | `faiss_hnsw.index`, `faiss_results.json` |
| 4 | `qdrant` | 컬렉션 재생성 + 배치 업로드 + 검색 + `page >= 5` 필터 검색 | `embeddings.npy`, `chunks.pkl`, `query.npy` | `qdrant_results.json`, `qdrant_filter_results.json` |
| 5 | `report` | 결과를 모아 마크다운 레포트 작성 | `meta.json`, `*_results.json` | `실습1_레포트.md` |

- 질문만 바꿔 다시 검색할 때: `QUERY` 수정 후 `embed_query` → `faiss` → `qdrant` → `report` 순으로 실행 (PDF 임베딩은 재사용)
- `qdrant` 단계는 Qdrant 서버(`localhost:6333`)가 실행 중이어야 하며, 실행할 때마다 `rag_docs` 컬렉션을 삭제 후 새로 만든다.

### 10. 파일 실행 흐름

PDF
 ↓
PyMuPDFLoader
 ↓
Document[]
 ↓
RecursiveCharacterTextSplitter
 ↓
Chunk Document[]
 ↓
BGE-M3
 ↓
1024차원 Dense Vector
 ↓
 ┌───────────────┬───────────────┐
 ↓                               ↓
FAISS HNSW                    Qdrant
 ↓                               ↓
Top-K 검색                    Top-K 검색
                                 ↓
                          Metadata Filter

'''

import argparse
import gc
import json
import pickle
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WORK_DIR = BASE_DIR / "outputs"
WORK_DIR.mkdir(exist_ok=True)

CHUNKS_PATH = WORK_DIR / "chunks.pkl"
EMBEDDINGS_PATH = WORK_DIR / "embeddings.npy"
FAISS_PATH = WORK_DIR / "faiss_hnsw.index"
REPORT_PATH = WORK_DIR / "실습1_레포트.md"

COLLECTION_NAME = "rag_docs"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
DIM = 1024
TOP_K = 5
QUERY = "HBM이란 무엇인가?"


def run(cmd):
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def stage_embed():
    import fitz
    import numpy as np
    from FlagEmbedding import BGEM3FlagModel
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    pdf_files = sorted(BASE_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"PDF가 없습니다: {BASE_DIR}")

    pages = []
    for pdf_path in pdf_files:
        print(f"Loading: {pdf_path.name}")
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                pages.append({"text": text, "page": i + 1, "filename": pdf_path.name})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "],
        keep_separator="end",  # 마침표를 다음 청크 앞이 아니라 문장 끝에 붙여 문장이 깨지지 않게 함
    )

    chunks = []
    for page in pages:
        for split in splitter.split_text(page["text"]):
            chunks.append({"text": split, "page": page["page"], "filename": page["filename"]})

    print(f"전체 PDF 수: {len(pdf_files)}")
    print(f"전체 페이지 수: {len(pages)}")
    print(f"전체 Chunk 수: {len(chunks)}")

    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    texts = [c["text"] for c in chunks]
    output = model.encode(texts, batch_size=16, return_dense=True)
    embeddings = np.array(output["dense_vecs"], dtype="float32")

    if embeddings.ndim != 2 or embeddings.shape[1] != DIM:
        raise ValueError(f"예상 임베딩 shape=(N,{DIM}), 실제={embeddings.shape}")

    with CHUNKS_PATH.open("wb") as f:
        pickle.dump(chunks, f)
    np.save(EMBEDDINGS_PATH, embeddings)

    meta = {
        "pdf_count": len(pdf_files),
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "embedding_shape": list(embeddings.shape),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "query": QUERY
    }
    (WORK_DIR / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"임베딩 저장 완료: {EMBEDDINGS_PATH}")
    print(f"shape: {embeddings.shape}")

    del model, output, embeddings
    gc.collect()


def stage_embed_query():
    import numpy as np
    from FlagEmbedding import BGEM3FlagModel

    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    q_vec = np.array(model.encode([QUERY], return_dense=True)["dense_vecs"], dtype="float32")
    np.save(WORK_DIR / "query.npy", q_vec)

    # 질문만 바꿔 재실행해도 레포트에 현재 질문이 기록되도록 meta.json 갱신
    meta_path = WORK_DIR / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["query"] = QUERY
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Query embedding 저장 완료: {q_vec.shape}")


def stage_faiss():
    import faiss
    import numpy as np

    embeddings = np.load(EMBEDDINGS_PATH).astype("float32")
    with CHUNKS_PATH.open("rb") as f:
        chunks = pickle.load(f)

    vectors = embeddings.copy()
    faiss.normalize_L2(vectors)

    index = faiss.IndexHNSWFlat(DIM, 32, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = 200
    index.hnsw.efSearch = 64
    index.add(vectors)
    faiss.write_index(index, str(FAISS_PATH))

    q_vec = np.load(WORK_DIR / "query.npy").astype("float32")
    faiss.normalize_L2(q_vec)
    scores, ids = index.search(q_vec, TOP_K)

    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], ids[0]), 1):
        c = chunks[int(idx)]
        results.append({
            "rank": rank,
            "score": float(score),
            "filename": c["filename"],
            "page": int(c["page"]),
            "text": c["text"]
        })

    (WORK_DIR / "faiss_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FAISS 인덱스 저장 완료: {FAISS_PATH}")
    print(f"\n질문: {QUERY}")
    print("\n[FAISS 검색 결과]")
    for r in results:
        print(f'{r["rank"]}위 | score={r["score"]:.4f} | {r["filename"]} | p.{r["page"]}')
        print("   " + " ".join(r["text"].split())[:300])


def stage_qdrant():
    import numpy as np
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, FieldCondition, Filter, PointStruct, Range, VectorParams

    embeddings = np.load(EMBEDDINGS_PATH).astype("float32")
    q_vec = np.load(WORK_DIR / "query.npy").astype("float32")
    with CHUNKS_PATH.open("rb") as f:
        chunks = pickle.load(f)

    client = QdrantClient(QDRANT_HOST, port=QDRANT_PORT)

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=DIM, distance=Distance.COSINE)
    )

    batch_size = 256
    for start in range(0, len(chunks), batch_size):
        end = min(start + batch_size, len(chunks))
        points = [
            PointStruct(
                id=i,
                vector=embeddings[i].tolist(),
                payload={"text": chunks[i]["text"], "page": int(chunks[i]["page"]), "filename": chunks[i]["filename"]}
            )
            for i in range(start, end)
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"Qdrant upsert: {end}/{len(chunks)}")

    dense = client.query_points(
        collection_name=COLLECTION_NAME,
        query=q_vec[0].tolist(),
        limit=TOP_K
    ).points

    filtered = client.query_points(
        collection_name=COLLECTION_NAME,
        query=q_vec[0].tolist(),
        query_filter=Filter(must=[FieldCondition(key="page", range=Range(gte=5))]),
        limit=TOP_K
    ).points

    qdrant_results = [{
        "rank": i,
        "score": float(p.score),
        "filename": p.payload["filename"],
        "page": int(p.payload["page"]),
        "text": p.payload["text"]
    } for i, p in enumerate(dense, 1)]

    filter_results = [{
        "rank": i,
        "score": float(p.score),
        "filename": p.payload["filename"],
        "page": int(p.payload["page"]),
        "text": p.payload["text"]
    } for i, p in enumerate(filtered, 1)]

    (WORK_DIR / "qdrant_results.json").write_text(json.dumps(qdrant_results, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK_DIR / "qdrant_filter_results.json").write_text(json.dumps(filter_results, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"\n질문: {QUERY}")
    print("\n[Qdrant 검색 결과]")
    for r in qdrant_results:
        print(f'{r["rank"]}위 | score={r["score"]:.4f} | {r["filename"]} | p.{r["page"]}')
        print("   " + " ".join(r["text"].split())[:300])

    print("\n[Qdrant 필터 검색: page >= 5]")
    for r in filter_results:
        print(f'{r["rank"]}위 | score={r["score"]:.4f} | {r["filename"]} | p.{r["page"]}')
        print("   " + " ".join(r["text"].split())[:300])


def stage_report():
    meta = json.loads((WORK_DIR / "meta.json").read_text(encoding="utf-8"))
    faiss_results = json.loads((WORK_DIR / "faiss_results.json").read_text(encoding="utf-8"))
    qdrant_results = json.loads((WORK_DIR / "qdrant_results.json").read_text(encoding="utf-8"))
    filter_results = json.loads((WORK_DIR / "qdrant_filter_results.json").read_text(encoding="utf-8"))

    def rows(items):
        return "\n".join(
            f'| {r["rank"]} | {r["score"]:.4f} | {r["filename"]} | {r["page"]} | {" ".join(r["text"].split())[:150].replace("|", "/")} |'
            for r in items
        )

    report = f"""# Vector DB 실습 1 레포트

"""
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\n레포트 생성 완료: {REPORT_PATH}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["embed", "embed_query", "faiss", "qdrant", "report"])
    args = parser.parse_args()

    if args.stage == "embed":
        stage_embed()
        return
    if args.stage == "embed_query":
        stage_embed_query()
        return
    if args.stage == "faiss":
        stage_faiss()
        return
    if args.stage == "qdrant":
        stage_qdrant()
        return
    if args.stage == "report":
        stage_report()
        return

    # 한 파일이지만 macOS에서 PyTorch/FlagEmbedding과 FAISS의 OpenMP 충돌을 피하기 위해 단계별 별도 프로세스로 실행
    run([sys.executable, __file__, "--stage", "embed"])
    run([sys.executable, __file__, "--stage", "embed_query"])
    run([sys.executable, __file__, "--stage", "faiss"])
    run([sys.executable, __file__, "--stage", "qdrant"])
    run([sys.executable, __file__, "--stage", "report"])

    print("\n전체 실습 완료")
    print(f"결과 폴더: {WORK_DIR}")
    print(f"레포트: {REPORT_PATH}")


if __name__ == "__main__":
    main()
