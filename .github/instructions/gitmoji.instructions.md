# Gitmoji Commit Message Format

커밋 메시지에 **Gitmoji**를 더해, 변경의 성격을 한눈에 알 수 있도록 하세요. Conventional Commits 규칙과 함께 사용하면 기록이 명확하고 즐거워집니다.

---

## Format

```
<emoji> <type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

* **emoji**: 변경 종류를 나타내는 Gitmoji 하나.
* **type**: `feat`, `fix`, `docs` … 와 같은 Conventional Commit 타입.
* **scope**: 영향 범위(모듈·폴더 등)를 괄호로 표기하며 생략 가능.
* **subject**: 50자 이내, 명령형 현재 시제, 첫 글자 소문자, 마침표 금지.
* 한글 커밋도 허용하지만 `emoji`, `type`, `scope` 는 그대로 유지합니다.

---

## Emoji ↔︎ Type 매핑

* ✨ **feat** — 새로운 기능 (SemVer *minor*)
* 🐛 **fix** — 버그 수정 (SemVer *patch*)
* 📝 **docs** — 문서만의 변경
* 🎨 **style** — 포맷·세미콜론 등 논리적 변경 없는 코드 스타일 수정
* ♻️ **refactor** — 리팩터링 (기능 추가·버그 수정 아님)
* ⚡️ **perf** — 성능 개선
* ✅ **test** — 테스트 추가·수정
* 🏗 **build** — 빌드 시스템·외부 의존성 변경
* 👷 **ci** — CI 설정·스크립트 변경
* 🔧 **chore** — 잡무(빌드 설정, 의존성 업데이트 등)
* ⏪ **revert** — 이전 커밋 되돌리기