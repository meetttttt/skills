# Sample Smoke-Test Generation Transcript

This transcript demonstrates how the **Smoke-Test** skill extracts requirements, inspects implemented code, generates automated test cases, and verifies execution.

---

### Step 1: Context Resolution (ClickUp / PRD / FRD)

**User**:  
> Please create and run smoke tests for our `slugify()` utility based on ClickUp task `CU-8675309`.

**Agent**:  
1. **Resolving Context**:
   - Priority 1: Found ClickUp Task ID `CU-8675309`.
   - Executing task fetch: `clickup_helper.py get CU-8675309`
2. **Requirements Extracted**:
   - **REQ-1**: Preserve non-Latin characters (Chinese, Cyrillic, Spanish) in UTF-8.
   - **REQ-2**: Replace spaces with single dashes and strip special punctuation (`!`, `?`).
   - **REQ-3**: Handle edge inputs (`""`, `null`, `undefined`) safely without throwing exceptions.

---

### Step 2: Codebase & Test Framework Inspection

**Agent**:  
1. **Codebase Inspection**:
   - Examined `src/utils.py`. Found `def slugify(text: str) -> str:`.
2. **Test Framework Detection**:
   - Detected `pytest` configuration in repository (`pyproject.toml`).

---

### Step 3: Smoke Test Suite Generation

**Agent**:  
Created `tests/test_smoke_slugify.py`:

```python
import pytest
from src.utils import slugify

class TestSlugifySmokeSuite:
    def test_req1_unicode_preservation(self):
        assert slugify("Hello 世界") == "hello-世界"
        assert slugify("Café y Música") == "café-y-música"

    def test_req2_punctuation_and_whitespace(self):
        assert slugify("  Hello!!!   World???  ") == "hello-world"

    def test_req3_edge_case_inputs(self):
        assert slugify("") == ""
        assert slugify(None) == ""
```

---

### Step 4: Automated Verification Execution

**Agent**:  
Running verification command: `pytest tests/test_smoke_slugify.py`

```text
============================= test session starts ==============================
collected 3 items

tests/test_smoke_slugify.py ...                                         [100%]

============================== 3 passed in 0.04s ===============================
```

**Summary Output**:
> ✅ **Smoke Test Suite Complete**
> - **Resolved Spec Source**: ClickUp Task `CU-8675309`
> - **Generated Test File**: `tests/test_smoke_slugify.py`
> - **Test Framework**: `pytest`
> - **Verification Result**: 3/3 smoke tests passing (100% pass rate).
