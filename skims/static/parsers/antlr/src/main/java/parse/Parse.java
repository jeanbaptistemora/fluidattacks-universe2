import com.google.gson.*;
import com.google.gson.stream.*;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.lang.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.regex.Pattern;
import java.util.Scanner;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;

public class Parse {

  private static final Pattern ALL = Pattern.compile("\\A");

  public static void traverse(
    JsonWriter json,
    ParseTree tree,
    Vocabulary vocabulary
  ) throws IOException {
    if (tree instanceof TerminalNodeImpl) {
      Token token = ((TerminalNodeImpl) tree).getSymbol();

      json.beginObject();
      json.name("c").value(token.getCharPositionInLine());
      json.name("l").value(token.getLine());
      json.name("text").value(token.getText());
      json.name("type").value(vocabulary.getSymbolicName(token.getType()));
      json.endObject();
      json.flush();
    }
    else {
      String name = tree.getClass().getSimpleName().replaceAll("Context$", "");

      json.beginObject();
      json.name(name).beginArray();
      for (int i = 0; i < tree.getChildCount(); i++) {
        traverse(json, tree.getChild(i), vocabulary);
      }
      json.endArray();
      json.endObject();
      json.flush();
    }
  }

  public static void main(String[] args) {
    try {
      // Read Stdin until EOF
      Scanner scanner = new Scanner(System.in);
      String source;
      try {
        source = scanner.useDelimiter(ALL).next();
      } catch (NoSuchElementException e) {
        source = "";
      }

      // Do the parsing
      CharStream charStream = CharStreams.fromString(source);
      JsonWriter json = new JsonWriter(new OutputStreamWriter(System.out));
      ParseTree tree;
      Vocabulary vocabulary;

      switch (args[0]) {
      case "Java9":
        Java9Lexer lexer = new Java9Lexer(charStream);
        Java9Parser parser = new Java9Parser(new CommonTokenStream(lexer));
        lexer.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parser.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parser.setTrimParseTree(true);
        parser.setErrorHandler(new BailErrorStrategy());
        vocabulary = parser.getVocabulary();
        tree = parser.compilationUnit();
        break;
      default:
        throw new ArrayIndexOutOfBoundsException("Invalid parser selected");
      }

      traverse(json, tree, vocabulary);

      System.exit(0);
    } catch (ArrayIndexOutOfBoundsException e) {
      System.err.println("Invalid arguments");
      System.exit(1);
    } catch (OutOfMemoryError e) {
      System.err.println("Not enough memory could be allocated");
      System.exit(1);
    } catch (IOException e) {
      System.err.println("Bad JSON stream");
      System.exit(1);
    } catch (ParseCancellationException e) {
      System.err.println("Content does not match grammar");
      System.exit(1);
    }
  }
}
