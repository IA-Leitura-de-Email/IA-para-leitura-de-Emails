import Enums.KnowledgeType;
import java.io.File;
import java.time.LocalDateTime;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

/*O Maven é tipo o gradle, ele serve para
 Gerenciamento de dependências
 Build do projeto
 Padronização de estrutura

 Sem o Maven, seria necessário baixar os arquivos para leituras
 de PDF manualmente. Com o Maven não é preciso, ele já faz este
 procedimento sozinho
 */

import java.util.List;

public class KnowledgeEntry {

    //Dados do arquivo:
    private String titulo;
    private KnowledgeType tipo;

    //Local do arquivo
    private String filePatch; //Onde fica o arquivo
    private String content; //Texto extraído

    //Onde o arquivo vem
    private String sourceUrl;

    //Palavras chaves para ajudar a IA na procura
    private List<String> palavrasChaves;
}
