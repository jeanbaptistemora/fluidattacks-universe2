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
      case "CSharp":
        CSharpLexer lexerCSharp = new CSharpLexer(charStream);
        CSharpParser parserCSharp = new CSharpParser(new CommonTokenStream(lexerCSharp));
        lexerCSharp.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parserCSharp.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parserCSharp.setTrimParseTree(true);
        parserCSharp.setErrorHandler(new BailErrorStrategy());
        vocabulary = parserCSharp.getVocabulary();
        tree = parserCSharp.compilation_unit();
        break;
      case "Java9":
        Java9Lexer lexerJava9 = new Java9Lexer(charStream);
        Java9Parser parserJava9 = new Java9Parser(new CommonTokenStream(lexerJava9));
        lexerJava9.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parserJava9.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parserJava9.setTrimParseTree(true);
        parserJava9.setErrorHandler(new BailErrorStrategy());
        vocabulary = parserJava9.getVocabulary();
        tree = parserJava9.compilationUnit();
        break;
      case "Scala":
        ScalaLexer lexerScala = new ScalaLexer(charStream);
        ScalaParser parserScala = new ScalaParser(new CommonTokenStream(lexerScala));
        lexerScala.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parserScala.removeErrorListener(ConsoleErrorListener.INSTANCE);
        parserScala.setTrimParseTree(true);
        parserScala.setErrorHandler(new BailErrorStrategy());
        vocabulary = parserScala.getVocabulary();
        tree = parserScala.compilationUnit();
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
