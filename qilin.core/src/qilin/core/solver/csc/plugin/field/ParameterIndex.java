package qilin.core.solver.csc.plugin.field;

import pascal.taie.collection.Maps;
import qilin.core.pag.LocalVarNode;
import qilin.core.pag.VarNode;
import soot.Value;
import soot.jimple.InstanceInvokeExpr;
import soot.jimple.InvokeExpr;
import soot.jimple.Stmt;
import soot.jimple.toolkits.callgraph.Edge;

import javax.annotation.Nullable;
import java.util.Map;
import java.util.Objects;

public record ParameterIndex(boolean isThis, int index) {
    public static ParameterIndex THISINDEX = new ParameterIndex(true, 0);
    public static Map<Integer, ParameterIndex> realParameters = Maps.newMap();

    @Override
    public String toString() {
        return isThis ? "%this" : index + "@parameter";
    }

    public static ParameterIndex getRealParameterIndex(int index) {
        return realParameters.computeIfAbsent(index, i -> new ParameterIndex(false, i));
    }


    @Nullable
    public static Value getCorrespondingArgument(Edge edge, ParameterIndex parameterIndex){
        Stmt stmt = (Stmt) edge.srcUnit();
        InvokeExpr invokeExpr = stmt.getInvokeExpr();
        if(!parameterIndex.isThis()){
            return invokeExpr.getArg(parameterIndex.index());
        }else if(invokeExpr instanceof InstanceInvokeExpr instanceInvokeExpr){
            return instanceInvokeExpr.getBase();
        }
        return null;
    }

    @Override
    public int hashCode() {
        return Objects.hash(isThis, index);
    }
}
