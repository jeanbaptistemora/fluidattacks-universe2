import com.google.gson.*;
import java.io.IOException;
import java.lang.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;

public class Ast {

  private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

  public static Map<String, Object> toMap(ParseTree tree, Vocabulary vocabulary) {
    Map<String, Object> map = new LinkedHashMap<>();
    traverse(tree, vocabulary, map);
    return map;
  }

  public static void traverse(ParseTree tree, Vocabulary vocabulary, Map<String, Object> map) {
    if (tree instanceof TerminalNodeImpl) {
      Token token = ((TerminalNodeImpl) tree).getSymbol();
      int type = token.getType();
      map.put("c", token.getCharPositionInLine());
      map.put("l", token.getLine());
      map.put("text", token.getText());
      map.put("type", vocabulary.getSymbolicName(type));
    }
    else {
      List<Map<String, Object>> children = new ArrayList<>();
      String name = tree.getClass().getSimpleName().replaceAll("Context$", "");
      map.put(name, children);

      for (int i = 0; i < tree.getChildCount(); i++) {
        Map<String, Object> nested = new LinkedHashMap<>();
        children.add(nested);
        traverse(tree.getChild(i), vocabulary, nested);
      }
    }
  }

  public static void main(String[] args) {
    try {
      String source = new String(Files.readAllBytes(Paths.get(args[1])));
      CharStream charStream = CharStreams.fromString(source);
      ParseTree tree;

      switch (args[0]) {
      case "Java9":
        Java9Lexer lexer = new Java9Lexer(charStream);
        Java9Parser parser = new Java9Parser(new CommonTokenStream(lexer));
        tree = parser.compilationUnit();
        break;
      default:
        throw new ArrayIndexOutOfBoundsException("Invalid parser selected");
      }

      System.out.println(GSON.toJson(toMap(tree, Java9Parser.VOCABULARY)));
      System.exit(0);
    } catch (ArrayIndexOutOfBoundsException e) {
      System.err.println("Invalid arguments");
      System.exit(1);
    } catch (IOException e) {
      System.err.println("Invalid file path, encoding or contents");
      System.exit(1);
    }
  }
}
