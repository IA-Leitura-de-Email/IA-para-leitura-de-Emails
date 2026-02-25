import java.time.LocalDate;
import java.time.LocalDateTime;

public class Email {

    //Aributos dos Emails:
    private long id;
    private LocalDateTime dataRecebimento;
    private String remetente;
    private String assunto;
    private String destinatario;
    private EmailStatus status;
    private String corpo;

    //Constructor:

    public Email(String remetente, String assunto,
                 String destinatario, EmailStatus status, String mensagem) {
        this.remetente = remetente;
        this.assunto = assunto;
        this.destinatario = destinatario;
        this.status = status;
        this.corpo = mensagem;
    }
}