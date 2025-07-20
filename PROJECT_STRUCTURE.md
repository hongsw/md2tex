# md2tex / md2x 프로젝트 구조 설명

## 📁 디렉토리 구조

```
Specification-Driven Parallel Agent Framework.../
├── 📄 논문 파일들 (프로젝트 루트)
│   ├── SDPAF_Academic_Paper.md      # 메인 논문 (Markdown)
│   ├── main.tex                     # LaTeX 버전
│   ├── references.bib               # 참고문헌
│   ├── Makefile                     # 🎯 변환 자동화 (make 명령)
│   ├── convert.sh                   # 🚀 원클릭 변환 스크립트
│   └── QUICK_START.md              # 빠른 시작 가이드
│
└── 📂 md2tex/                       # 변환 도구
    ├── md2x.py                      # ✨ 메인 변환 프로그램
    ├── md2tex.py                    # 기존 버전 (호환성)
    ├── setup.py                     # 패키지 설정
    ├── requirements.txt             # 필요한 패키지들
    │
    ├── 📂 utils/                    # 핵심 변환 모듈
    │   ├── converters.py            # 기본 MD→TeX 변환기
    │   ├── arxiv_converters.py      # ✨ ArXiv 특화 변환기
    │   ├── arxiv_template.tex       # ✨ ArXiv 템플릿
    │   └── template.tex             # 기본 템플릿
    │
    └── 📂 examples/                 # 예제 파일들
        └── sample_paper.md          # 예제 논문
```

## 🔧 주요 파일 설명

### 1. **md2x.py** (메인 변환 도구)
```bash
# 사용법
python3 md2x.py input.md -f pdf    # PDF로 변환
python3 md2x.py input.md -f html   # HTML로 변환
python3 md2x.py input.md -f arxiv  # ArXiv 패키지 생성
```

**주요 기능:**
- 다중 출력 형식: tex, pdf, html, docx, arxiv
- 실시간 감시 모드 (--watch)
- ArXiv 최적화 (--arxiv)
- 사용자 정의 템플릿

### 2. **utils/arxiv_converters.py** (ArXiv 변환기)
- **ArxivMetadata**: 제목, 저자, 초록 추출
- **ArxivTable**: Markdown 표 → LaTeX 표 변환
- **ArxivMath**: 수식 변환 ($...$, $$...$$)
- **ArxivCitation**: 인용 처리 ([1], [Author2023])

### 3. **Makefile** (자동화)
```bash
make            # 모든 형식으로 변환
make pdf        # PDF만
make arxiv      # ArXiv 패키지
make watch      # 실시간 변환
```

## 🚀 사용 방법

### 1. 가장 간단한 방법
```bash
# 프로젝트 루트에서
./convert.sh
```

### 2. Make 사용
```bash
# 프로젝트 루트에서
make
```

### 3. 직접 실행
```bash
# md2tex 폴더에서
python3 md2x.py ../SDPAF_Academic_Paper.md -f pdf
```

## 📦 설치 방법

```bash
# md2tex 폴더에서
pip3 install -e .

# 또는 프로젝트 루트에서
make install
```

## 🎯 개선 사항

### 완료된 개선사항:
1. ✅ **다중 출력 형식 지원** (tex, pdf, html, arxiv)
2. ✅ **ArXiv 특화 기능** (메타데이터, 표, 수식, 인용)
3. ✅ **원클릭 변환** (convert.sh, Makefile)
4. ✅ **실시간 감시 모드** (파일 변경 시 자동 변환)

### 향후 개선 계획:
1. 📝 더 많은 저널 템플릿 추가
2. 🎨 스타일 커스터마이징 옵션
3. 📊 변환 품질 검증 도구
4. 🌐 웹 인터페이스 추가

## 💡 팁

1. **LaTeX 설치 확인** (PDF 생성에 필요)
   ```bash
   which pdflatex
   ```

2. **Python 버전 확인** (3.7+ 필요)
   ```bash
   python3 --version
   ```

3. **변환 결과 확인**
   ```bash
   ls -la output/
   ```

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 문의

- Email: seungwoo.hong@baryon.ai
- GitHub: https://github.com/hongsw/md2tex