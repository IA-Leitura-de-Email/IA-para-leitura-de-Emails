```md

Possível estrutura visual pelos meus estudos:

domain
├── model
│   ├── Email                 // Mensagem
│   ├── Usuario               // Usuário logado
│   ├── KnowledgeEntry        // Onde ficam os manuais
│   ├── Approval              // Aprovação Humana
│   ├── AuditLog              // Registro de tudo
│   └── FaultTreeNode         // Testes que podem ser indicados
│
└── enum
    ├── EmailStatus           // Status atual do Email
    ├── KnowledgeType         // Manual, Árvore de falha, Procedimento
    └── ApprovalStatus        // Resultado da análise Humana

engine (IA)
├── DecisionEngine
└── RuleBasedDecisionEngine   // Consulta a base

service
├── EmailProcessingService    // Recebe emails, atualiza status (coordena tudo)
├── KnowledgeService          // Ponte entre engine e domain
├── ApprovalWorkflowService   // Controla a aprovação
└── MetricsService            // Calcula tempo de resposta

repository
├── EmailRepository           // Salva email, atualiza registro
├── KnowledgeRepository       // Salva conhecimento
├── UserRepository            // Salva usuário
├── ApprovalRepository        // Registra aprovações
└── AuditLogRepository        // Registra eventos

´´´´´
´´
