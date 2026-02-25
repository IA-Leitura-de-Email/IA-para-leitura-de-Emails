public class Usuario {

    //Atributos:
    private String nome;
    private String email;
    private String matricula;

    //Constructor:
    public Usuario(String nome, String email, String matricula) {
        this.nome = nome;
        this.email = email;
        this.matricula = matricula;
    }

    //Pega o email e determina como deve ser:
    public String getEmail() {return
            matricula + "@intelbras.com.br";}
    public String setEmail() {
        return String.format("%s" + "@intelbras.com.br", matricula);
    }
}
