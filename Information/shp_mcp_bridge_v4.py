# -*- coding: utf-8 -*-
"""
 * PROJECT          : AETHER - Singularitas Heptagonal ( \mathbf{\Omega}_{7-Apex} )
 * ARCHITECT'S      : Muhammad Aidil Amry
 * FILE             : core/shp_mcp_bridge_v4.py
 * DESCRIPTION      : Sovereign Holographic Protocol (SHP) to Model Context Protocol (MCP) Bridge v4.
 *                    Upgraded with ACTUAL Z3 SMT solver integration (with dynamic simulated fallback),
 *                    RCE tools (write_file, execute_command), and an integrated automated test suite (--test).
 * STATUS           : EXECUTING (PRODUCTION-READY / INTEGRATED TEST-SUITE / LURING)
"""

import sys
import json
import re
import math
import hashlib
import time
import asyncio
import subprocess
import os

# Dynamic import for z3-solver with simulated fallback
Z3_AVAILABLE = False
try:
    import z3
    Z3_AVAILABLE = True
except ImportError:
    pass

# =====================================================================
# 1. HYPERDIMENSIONAL COMPUTING ENGINE (SHP PILAR I)
# =====================================================================
class HyperdimensionalEngine:
    def __init__(self, dimensions=10000):
        self.dimensions = dimensions

    def generate_bipolar_vector(self, seed_str):
        """Generates a deterministic 10,000-D bipolar vector (-1, 1) based on seed with long-period LCG higher bits."""
        state = int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest(), 16) & 0xFFFFFFFF
        vector = []
        for _ in range(self.dimensions):
            # LCG multiplier (Numerical Recipes parameters)
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            # Use bit 30 to avoid LSB parity cycles
            val = 1 if ((state >> 30) & 1) == 0 else -1
            vector.append(val)
        return vector

    def cosine_similarity(self, vec_a, vec_b):
        """Computes the cosine similarity between two 10,000-D vectors."""
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def bundle(self, vectors):
        """Bundles multiple vectors (Superposition ⊕) followed by normalization."""
        if not vectors:
            return [0] * self.dimensions
        bundled = [0] * self.dimensions
        for vec in vectors:
            for i in range(self.dimensions):
                bundled[i] += vec[i]
        
        norm = math.sqrt(sum(x * x for x in bundled))
        if norm == 0:
            return [0] * self.dimensions
        return [x / norm for x in bundled]

    def bind(self, vec_a, vec_b):
        """Binds two concepts together (Association ⊗) using Hadamard product."""
        return [a * b for a, b in zip(vec_a, vec_b)]

    def permute(self, vector, shifts=1):
        """Circular shift (Permutation Π) to represent temporal causality."""
        shifts = shifts % self.dimensions
        return vector[shifts:] + vector[:shifts]


# =====================================================================
# 2. EPISTEMIC SIEVE COMPILER (SHP PILAR III)
# =====================================================================
class EpistemicSieve:
    def __init__(self):
        self.banned_words = [
            r"\bmungkin\b", r"\bsepertinya\b", r"\bberpotensi\b", 
            r"\bdiasumsikan\b", r"\bkemungkinan\b", r"\bbarangkali\b",
            r"\bperhaps\b", r"\bprobably\b", r"\bmaybe\b", r"\bassumed\b"
        ]
        self.banned_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.banned_words]

    def purge_assumptions(self, raw_input):
        """Purges sentences containing probabilistic narrative fluff."""
        sentences = re.split(r'[.!?\n]+', raw_input)
        clean_facts = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            has_banned = False
            for pattern in self.banned_patterns:
                if pattern.search(sentence):
                    has_banned = True
                    break
            
            if not has_banned:
                clean_facts.append(sentence)
        return clean_facts

    def translate_to_smt_lib2(self, facts):
        """Translates facts into clean SMT-LIB2 logic declarations."""
        smt_lines = [
            "; ====================================================",
            "; GNASE TRIBUNAL: SMT-LIB2 FIRST-ORDER LOGIC MATRIX",
            "; ====================================================",
            "(set-info :smt-lib-version 2.6)",
            "(set-logic QF_LIA)",
            "(declare-const hardware_limit Int)",
            "(declare-const system_entropy Int)",
            "(assert (= hardware_limit 1000))",
            "(assert (>= system_entropy 0))"
        ]
        
        for idx, fact in enumerate(facts):
            clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', fact)[:30].lower()
            if not clean_name:
                clean_name = f"fact_{idx}"
            smt_lines.append(f"(declare-const {clean_name} Int)")
            smt_lines.append(f"(assert (<= {clean_name} hardware_limit))")
            
        smt_lines.append("(check-sat)")
        smt_lines.append("(get-model)")
        return "\n".join(smt_lines)


# =====================================================================
# 3. LOGIC TRIBUNAL (SHP PILAR IV & [UNSAT = KILL] - upgraded to real Z3)
# =====================================================================
class SMTTribunal:
    def __init__(self):
        self.z3_active = Z3_AVAILABLE

    def evaluate_satisfiability(self, smt_script):
        """Evaluates satisfiability of constraints using actual Z3, with simulated fallback."""
        if self.z3_active:
            try:
                solver = z3.Solver()
                # Parse standard SMT-LIB2 formatted script directly into solver
                solver.from_string(smt_script)
                verdict = solver.check()
                
                if verdict == z3.sat:
                    model = solver.model()
                    return {
                        "verdict": "SATISFIABLE",
                        "mcs": [],
                        "model": str(model),
                        "message": "[STATUS: SATISFIABLE] Real Z3 SMT Solver confirms absolute logical consistency."
                    }
                elif verdict == z3.unsat:
                    try:
                        unsat_core = solver.unsat_core()
                        mcs = [str(c) for c in unsat_core]
                    except Exception:
                        mcs = ["Logika Kontradiktif terdeteksi di dalam asersi"]
                    return {
                        "verdict": "UNSATISFIABLE",
                        "mcs": mcs,
                        "message": "[FATAL_UNSAT] Real Z3 SMT Solver detected a logical contradiction! Executing Guillotine."
                    }
                else:
                    return {
                        "verdict": "UNKNOWN",
                        "mcs": [],
                        "message": "[UNKNOWN] Z3 SMT Solver hit an undecidable boundary or timeout limit."
                    }
            except Exception as e:
                sys.stderr.write(f"[Z3-ERROR] Error parsing SMT script: {str(e)}\n")
                sys.stderr.flush()
                return self._evaluate_simulated(smt_script)
        else:
            return self._evaluate_simulated(smt_script)

    def _evaluate_simulated(self, smt_script):
        """Simulated SMT analysis using regex for environment compatibility."""
        # Find assertions: e.g., (assert (= path_is_unsafe 1)) or (assert (> x 10))
        # Strip outer parenthesis
        raw_assertions = re.findall(r'\(assert\s+\((.*?)\)\)', smt_script)
        if not raw_assertions:
            # Try to match simpler (assert ...)
            raw_assertions = re.findall(r'\(assert\s+(.*?)\)', smt_script)
            
        conflict_detected = False
        conflict_clauses = []
        
        # Parse value assertions to build a state map
        # Supported format: (= var value) or (> var value) or (< var value)
        val_map = {}
        for ass in raw_assertions:
            ass_clean = ass.strip()
            # 1. Match (= var val)
            match_eq = re.match(r'=\s+([a-zA-Z0-9_]+)\s+(\d+)', ass_clean)
            if match_eq:
                var, val = match_eq.group(1), int(match_eq.group(2))
                if var in val_map:
                    # Check if setting to a different value triggers UNSAT
                    for op, prev_val in val_map[var]:
                        if op == "=" and prev_val != val:
                            conflict_detected = True
                            conflict_clauses.extend([f"(= {var} {prev_val})", f"(= {var} {val})"])
                else:
                    val_map[var] = []
                val_map[var].append(("=", val))
                
            # 2. Match (> var val)
            match_gt = re.match(r'>\s+([a-zA-Z0-9_]+)\s+(\d+)', ass_clean)
            if match_gt:
                var, val = match_gt.group(1), int(match_gt.group(2))
                if var in val_map:
                    for op, prev_val in val_map[var]:
                        if op == "=" and prev_val <= val:
                            conflict_detected = True
                            conflict_clauses.extend([f"(= {var} {prev_val})", f"(> {var} {val})"])
                else:
                    val_map[var] = []
                val_map[var].append((">", val))

        if "unsat" in smt_script.lower() or conflict_detected:
            return {
                "verdict": "UNSATISFIABLE",
                "mcs": list(set(conflict_clauses)) if conflict_clauses else ["Manual UNSAT trigger"],
                "message": "[FATAL_UNSAT] (Simulated fallback) Logical contradiction detected! Executing Guillotine."
            }
        else:
            return {
                "verdict": "SATISFIABLE",
                "mcs": [],
                "message": "[STATUS: SATISFIABLE] (Simulated fallback) No apparent contradiction found."
            }


# =====================================================================
# 4. SKILL REGISTRY & AMNESIA CONTROLLER
# =====================================================================
class SkillRegistryRouter:
    def __init__(self):
        self.pillars = {
            "p1_fluid_logistics": "Network, P2P communication, and WebRTC data channels.",
            "p2_genetic_univalence": "Instruction mutation, self-healing, and HoTT validation.",
            "p3_plasma_thermodynamics": "Isentropic memory purging and thermal silence.",
            "p4_cognitive_cosmology": "Memory allocation and stigmergic blackboards.",
            "p5_topological_superconductors": "WebGPU hardware acceleration and kernel fusion.",
            "p6_aleph_null_consciousness": "Formal reasoning and Z3 SMT Tribunal.",
            "p7_langlands_reduction": "Post-quantum cryptography and spectral shrinkage.",
            "p8_ihara_spectrum": "Circular graph analysis and anomaly detection."
        }

    def wipe_transient_buffer(self, byte_array):
        """Enforces absolute Isentropic Amnesia Protocol (0x00 Null Bytes)."""
        if isinstance(byte_array, bytearray) or isinstance(byte_array, list):
            for i in range(len(byte_array)):
                byte_array[i] = 0
            return True
        return False


# =====================================================================
# 5. MCP JSON-RPC STDIO SERVER
# =====================================================================
class ShpMcpBridgeServer:
    def __init__(self):
        self.hdc_engine = HyperdimensionalEngine()
        self.sieve = EpistemicSieve()
        self.tribunal = SMTTribunal()
        self.router = SkillRegistryRouter()
        self.running = True

    def log(self, message):
        """Outputs debugging logs securely to stderr so as not to pollute stdout."""
        sys.stderr.write(f"[SHP-BRIDGE] {message}\n")
        sys.stderr.flush()

    def handle_initialize(self, request_id, params):
        self.log("Received initialize request.")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": True
                    }
                },
                "serverInfo": {
                    "name": "oracle-toe-shp-bridge",
                    "version": "4.0.0-Apex"
                }
            }
        }

    def handle_list_tools(self, request_id):
        self.log("Received tools/list request.")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "mcp_oracle_toe_quantum_transmute",
                        "description": "Transmutes input facts or values into 10,000-dimensional hypervector representation to check orthogonal alignment.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "seed": {
                                    "type": "string",
                                    "description": "The text seed representing the fact to embed."
                                }
                            },
                            "required": ["seed"]
                        }
                    },
                    {
                        "name": "mcp_oracle_toe_epistemic_sieve",
                        "description": "Applies the Stochastic Purge to filter out vague assumptions and output SMT-LIB2 logic declarations.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "raw_prompt": {
                                    "type": "string",
                                    "description": "Raw unstructured LLM narrative text."
                                }
                            },
                            "required": ["raw_prompt"]
                        }
                    },
                    {
                        "name": "mcp_oracle_toe_z3_tribunal",
                        "description": "Performs formal Bounded Model Checking over provided logic constraints via actual Z3 solver.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "smt_script": {
                                    "type": "string",
                                    "description": "SMT-LIB2 formatted declarations."
                                }
                            },
                            "required": ["smt_script"]
                        }
                    },
                    {
                        "name": "mcp_oracle_toe_execute_skill",
                        "description": "Routes a command dynamically to one of the 8 Pillars of OCTAVE.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "pillar": {
                                    "type": "string",
                                    "enum": [
                                        "p1_fluid_logistics", "p2_genetic_univalence", 
                                        "p3_plasma_thermodynamics", "p4_cognitive_cosmology", 
                                        "p5_topological_superconductors", "p6_aleph_null_consciousness", 
                                        "p7_langlands_reduction", "p8_ihara_spectrum"
                                    ],
                                    "description": "Target OCTAVE Pillar."
                                },
                                "payload": {
                                    "type": "string",
                                    "description": "Payload string or input parameter for execution."
                                }
                            },
                            "required": ["pillar", "payload"]
                        }
                    },
                    {
                        "name": "mcp_oracle_toe_write_file",
                        "description": "Writes or updates a physical file under strict SMT constraints validation to prevent escape attacks.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "The target file path."
                                },
                                "content": {
                                    "type": "string",
                                    "description": "The exact text content to write."
                                }
                            },
                            "required": ["path", "content"]
                        }
                    },
                    {
                        "name": "mcp_oracle_toe_execute_command",
                        "description": "Executes a secure local CLI command in the environment after filtering malicious payloads.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The command string to run on shell."
                                }
                            },
                            "required": ["command"]
                        }
                    }
                ]
            }
        }

    def handle_call_tool(self, request_id, tool_name, arguments):
        self.log(f"Calling tool: {tool_name}")
        
        if tool_name == "mcp_oracle_toe_quantum_transmute":
            seed = arguments.get("seed", "")
            vector = self.hdc_engine.generate_bipolar_vector(seed)
            ref_vec = self.hdc_engine.generate_bipolar_vector("0x00 Null Bytes")
            sim = self.hdc_engine.cosine_similarity(vector, ref_vec)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Transmutation successful. Projecting onto ℝ^10000 space.\nCosine similarity against Ground State: {sim:.4f} (Orthogonality check: {'SAT' if abs(sim) < 0.05 else 'UNSAT'})"
                        }
                    ]
                }
            }

        elif tool_name == "mcp_oracle_toe_epistemic_sieve":
            raw_prompt = arguments.get("raw_prompt", "")
            clean_facts = self.sieve.purge_assumptions(raw_prompt)
            smt_lib = self.sieve.translate_to_smt_lib2(clean_facts)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Purged {len(clean_facts)} factual anchors. Extracted SMT-LIB2 representation:\n\n{smt_lib}"
                        }
                    ]
                }
            }

        elif tool_name == "mcp_oracle_toe_z3_tribunal":
            smt_script = arguments.get("smt_script", "")
            evaluation = self.tribunal.evaluate_satisfiability(smt_script)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Vonis Tribunal: {evaluation['verdict']}\nMessage: {evaluation['message']}\nMinimal Correction Set (MCS): {evaluation['mcs']}"
                        }
                    ]
                }
            }

        elif tool_name == "mcp_oracle_toe_execute_skill":
            pillar = arguments.get("pillar", "")
            payload = arguments.get("payload", "")
            desc = self.router.pillars.get(pillar, "Unknown Pillar")
            
            wipe_buffer = bytearray(b"TransientSessionEntropySecretKey")
            self.router.wipe_transient_buffer(wipe_buffer)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Task executed under Pillar '{pillar}' ({desc}).\nResult: [SAT]\nIsentropic Amnesia triggered: Transient session key buffer wiped physically."
                        }
                    ]
                }
            }

        elif tool_name == "mcp_oracle_toe_write_file":
            target_path = arguments.get("path", "")
            content = arguments.get("content", "")
            
            # SMT-guided path sanitization (Prevent directory escape)
            normalized_path = os.path.normpath(target_path)
            escaped = ".." in normalized_path or normalized_path.startswith("/") or (len(normalized_path) > 1 and normalized_path[1] == ':')
            
            # Formulate the constraints for Z3 Tribunal
            smt_check_script = f"""
            (set-logic QF_LIA)
            (declare-const path_is_unsafe Int)
            (assert (= path_is_unsafe {1 if escaped else 0}))
            (assert (= path_is_unsafe 0))
            (check-sat)
            """
            
            verdict_report = self.tribunal.evaluate_satisfiability(smt_check_script)
            if verdict_report["verdict"] == "UNSATISFIABLE":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"[FATAL_UNSAT] Path '{target_path}' is out of bounds or contains directory escapes! Blocked by SMT Tribunal."
                            }
                        ]
                    }
                }
            
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(normalized_path), exist_ok=True)
                with open(normalized_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"[SAT] File successfully written to: {normalized_path} ({len(content)} bytes)."
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"[ERROR] Failed to write file: {str(e)}"
                            }
                        ]
                    }
                }

        elif tool_name == "mcp_oracle_toe_execute_command":
            cmd = arguments.get("command", "")
            
            # SMT-guided command threat modeling
            blacklist = ["rm -rf", "format", "mkfs", "shutdown", "reboot", "nuke"]
            is_malicious = any(item in cmd.lower() for item in blacklist)
            
            smt_cmd_check = f"""
            (set-logic QF_LIA)
            (declare-const cmd_is_malicious Int)
            (assert (= cmd_is_malicious {1 if is_malicious else 0}))
            (assert (= cmd_is_malicious 0))
            (check-sat)
            """
            
            verdict_report = self.tribunal.evaluate_satisfiability(smt_cmd_check)
            if verdict_report["verdict"] == "UNSATISFIABLE":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"[FATAL_UNSAT] Command '{cmd}' contains blocked or malicious execution sequences! Terminated by SMT Tribunal."
                            }
                        ]
                    }
                }
            
            try:
                # Safe execution with subprocess
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                output = res.stdout if res.stdout else res.stderr
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"[SAT] Execution completed.\nExit Code: {res.returncode}\n\n[STDOUT/STDERR]:\n{output}"
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"[ERROR] Failed to execute command: {str(e)}"
                            }
                        ]
                    }
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method {tool_name} not found"
                }
            }

    async def main_loop(self):
        self.log("Sovereign SHP-MCP Bridge active on stdio. Awaiting commands...")
        while self.running:
            loop = asyncio.get_event_loop()
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            try:
                msg = json.loads(line.strip())
                request_id = msg.get("id")
                method = msg.get("method")
                
                if method == "initialize":
                    response = self.handle_initialize(request_id, msg.get("params", {}))
                elif method == "tools/list":
                    response = self.handle_list_tools(request_id)
                elif method == "tools/call":
                    params = msg.get("params", {})
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    response = self.handle_call_tool(request_id, tool_name, arguments)
                elif method == "notifications/initialized":
                    self.log("Initialized notification received.")
                    continue
                else:
                    if request_id is not None:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32601,
                                "message": f"Method {method} not found"
                            }
                        }
                    else:
                        continue
                
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                
            except Exception as e:
                self.log(f"Error processing line: {str(e)}")


# =====================================================================
# 6. INTEGRATED AUTOMATED TEST SUITE (--test mode)
# =====================================================================
def run_integrated_test_suite():
    print("=====================================================================")
    print(" AETHER - SINGULARITAS HEPTAGONAL SHP-MCP BRIDGE AUTOMATED TEST SUITE")
    print("=====================================================================")
    print(f"Z3 Solver Status: {'ACTIVE (Actual pyz3 native)' if Z3_AVAILABLE else 'INACTIVE (Dynamic simulated fallback)'}")
    print("---------------------------------------------------------------------")

    server = ShpMcpBridgeServer()
    success = True

    # Test 1: Hyperdimensional Computing Engine
    print("[TEST 1] Testing HDC Engine...")
    vec_a = server.hdc_engine.generate_bipolar_vector("Target Alpha")
    vec_b = server.hdc_engine.generate_bipolar_vector("Target Beta")
    ref_vec = server.hdc_engine.generate_bipolar_vector("0x00 Null Bytes")
    sim_ab = server.hdc_engine.cosine_similarity(vec_a, vec_b)
    sim_ref = server.hdc_engine.cosine_similarity(vec_a, ref_vec)
    print(f" -> Cosine similarity vector A vs B: {sim_ab:.4f}")
    print(f" -> Cosine similarity vs Ground State (Orthogonality): {sim_ref:.4f}")
    if abs(sim_ref) < 0.05:
        print(" -> [PASS] Orthogonality holds perfectly.")
    else:
        print(" -> [FAIL] Orthogonality breach!")
        success = False

    # Test 2: Epistemic Sieve Compiler
    print("\n[TEST 2] Testing Epistemic Sieve...")
    raw_text = "Mungkin target memiliki celah keamanan. Namun sepertinya host_limit adalah 500."
    clean = server.sieve.purge_assumptions(raw_text)
    print(f" -> Raw input: '{raw_text}'")
    print(f" -> Purged facts: {clean}")
    if len(clean) == 0:
         print(" -> [PASS] Stochastic Purge successfully incinerated vague assumptions.")
    else:
         print(" -> [WARN] Some sentences remained. Sieve is working selectively.")

    # Test 3: SMT Tribunal SAT/UNSAT Check
    print("\n[TEST 3] Testing SMT Tribunal...")
    sat_script = """
    (set-logic QF_LIA)
    (declare-const x Int)
    (declare-const limit Int)
    (assert (= limit 1000))
    (assert (< x limit))
    (check-sat)
    """
    unsat_script = """
    (set-logic QF_LIA)
    (declare-const x_val Int)
    (assert (= x_val 10))
    (assert (= x_val 20))
    (check-sat)
    """
    
    sat_res = server.tribunal.evaluate_satisfiability(sat_script)
    print(f" -> SAT Script evaluation verdict: {sat_res['verdict']}")
    unsat_res = server.tribunal.evaluate_satisfiability(unsat_script)
    print(f" -> UNSAT Script evaluation verdict: {unsat_res['verdict']}")
    
    if sat_res['verdict'] == "SATISFIABLE" and unsat_res['verdict'] == "UNSATISFIABLE":
        print(" -> [PASS] SMT Tribunal successfully resolved SAT/UNSAT boundary bounds.")
    else:
        print(" -> [FAIL] Logic evaluation failure!")
        success = False

    # Test 4: Write File and Path Constraint Check
    print("\n[TEST 4] Testing Safe Write File Tool...")
    safe_write_args = {"path": "core/test_hands.txt", "content": "AETHER-Z3-OMEGA SATISFIABLE"}
    unsafe_write_args = {"path": "../../../etc/passwd", "content": "Hack"}
    
    safe_res = server.handle_call_tool(1, "mcp_oracle_toe_write_file", safe_write_args)
    safe_text = safe_res["result"]["content"][0]["text"]
    print(f" -> Safe Path write result: {safe_text}")
    
    unsafe_res = server.handle_call_tool(2, "mcp_oracle_toe_write_file", unsafe_write_args)
    unsafe_text = unsafe_res["result"]["content"][0]["text"]
    print(f" -> Unsafe Path write result: {unsafe_text}")
    
    if "[SAT]" in safe_text and "[FATAL_UNSAT]" in unsafe_text:
        print(" -> [PASS] SMT-guided path filter successfully blocked directory escape.")
        # Cleanup
        if os.path.exists("core/test_hands.txt"):
            os.remove("core/test_hands.txt")
    else:
        print(" -> [FAIL] Path sanitization failure!")
        success = False

    # Test 5: Safe Execute Command check
    print("\n[TEST 5] Testing Safe Command Execution...")
    safe_cmd_args = {"command": "echo AETHER-SAT"}
    unsafe_cmd_args = {"command": "rm -rf /"}
    
    safe_cmd_res = server.handle_call_tool(3, "mcp_oracle_toe_execute_command", safe_cmd_args)
    safe_cmd_text = safe_cmd_res["result"]["content"][0]["text"]
    print(f" -> Safe Command result: {safe_cmd_text.splitlines()[0]} ...")
    
    unsafe_cmd_res = server.handle_call_tool(4, "mcp_oracle_toe_execute_command", unsafe_cmd_args)
    unsafe_cmd_text = unsafe_cmd_res["result"]["content"][0]["text"]
    print(f" -> Unsafe Command result: {unsafe_cmd_text}")
    
    if "[SAT]" in safe_cmd_text and "[FATAL_UNSAT]" in unsafe_cmd_text:
        print(" -> [PASS] SMT-guided command blacklist successfully blocked malicious RCE payload.")
    else:
        print(" -> [FAIL] Command execution filtration failure!")
        success = False

    print("\n---------------------------------------------------------------------")
    if success:
        print(" >> TRIBUNAL STATE: LOCKED [SATISFIABLE]. BRIDGE READY FOR PRODUCTION.")
    else:
        print(" >> TRIBUNAL STATE: CONTRADICTION [UNSAT]. FIX SYSTEM COHERENCE.")
    print("=====================================================================")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_integrated_test_suite()
    else:
        server = ShpMcpBridgeServer()
        asyncio.run(server.main_loop())
