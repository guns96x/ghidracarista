// Ghidra Headless / GUI Script for Automated Evidence Extraction
//@author Antigravity Clean-Room Protocol Engine
//@category VAG.Diagnostics
//@keybinding
//@menupath
//@toolbar

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.data.DataType;
import ghidra.program.model.mem.MemoryAccessException;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.*;

public class ExportEvidence extends GhidraScript {

    @Override
    public void run() throws Exception {
        println("=== Starting VAG Diagnostic Evidence Exporter ===");

        File outDir = new File(getProjectRootFolder().getProjectLocator().getLocation(), "research/ghidra_export");
        if (!outDir.exists()) {
            outDir.mkdirs();
        }

        File outFile = new File(outDir, "ghidra_evidence_symbols.json");
        PrintWriter writer = new PrintWriter(new FileWriter(outFile));

        writer.println("{");
        writer.println("  \"program\": \"" + currentProgram.getName() + "\",");
        writer.println("  \"creation_date\": \"" + new Date().toString() + "\",");
        writer.println("  \"functions\": [");

        FunctionIterator functions = currentProgram.getFunctionManager().getFunctions(true);
        boolean firstFunc = true;

        int count = 0;
        while (functions.hasNext() && !monitor.isCancelled()) {
            Function func = functions.next();
            String name = func.getName();
            String demangled = (func.getSignature() != null) ? func.getSignature().getPrototypeString() : name;
            Address entry = func.getEntryPoint();

            // Filter for diagnostic relevant functions
            if (isDiagnosticRelevant(name) || isDiagnosticRelevant(demangled)) {
                if (!firstFunc) {
                    writer.println(",");
                }
                firstFunc = false;

                writer.println("    {");
                writer.println("      \"address\": \"" + entry.toString() + "\",");
                writer.println("      \"name\": \"" + escapeJson(name) + "\",");
                writer.println("      \"signature\": \"" + escapeJson(demangled) + "\",");
                writer.println("      \"callers\": [");

                Reference[] callingRefs = getReferencesTo(entry);
                boolean firstCaller = true;
                for (Reference ref : callingRefs) {
                    if (ref.getReferenceType().isCall()) {
                        if (!firstCaller) writer.print(", ");
                        firstCaller = false;
                        writer.print("\"" + ref.getFromAddress().toString() + "\"");
                    }
                }
                writer.println("],");

                writer.println("      \"referenced_strings\": [");
                boolean firstStr = true;
                InstructionIterator instructions = currentProgram.getListing().getInstructions(func.getBody(), true);
                while (instructions.hasNext()) {
                    Instruction instr = instructions.next();
                    Reference[] refs = instr.getReferencesFrom();
                    for (Reference r : refs) {
                        Data data = getDataAt(r.getToAddress());
                        if (data != null && data.hasStringValue()) {
                            if (!firstStr) writer.print(", ");
                            firstStr = false;
                            writer.print("\"" + escapeJson(data.getValue().toString()) + "\"");
                        }
                    }
                }
                writer.println("]");
                writer.print("    }");
                count++;
            }
        }

        writer.println("\n  ]");
        writer.println("}");
        writer.close();

        println("Exported " + count + " diagnostic functions to " + outFile.getAbsolutePath());
    }

    private boolean isDiagnosticRelevant(String str) {
        if (str == null) return false;
        String s = str.toLowerCase();
        return s.contains("vag") || s.contains("uds") || s.contains("kwp") ||
               s.contains("elm") || s.contains("stn") || s.contains("can") ||
               s.contains("isotp") || s.contains("troublecode") || s.contains("adaptation") ||
               s.contains("coding") || s.contains("basicsetting") || s.contains("routine") ||
               s.contains("dpf") || s.contains("parkingbrake") || s.contains("batteryreg") ||
               s.contains("livedata");
    }

    private String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\b", "\\b")
                .replace("\f", "\\f")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }
}
