import Enums.KnowledgeType;
import java.io.File;
import java.time.LocalDateTime;


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
