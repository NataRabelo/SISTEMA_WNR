from flask_login import UserMixin
from app.extensions import db


class Sexo(db.Model):
    __tablename__ = "sexo"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    clientes                        = db.relationship("Cliente", back_populates="sexo")


class CondicaoHabitacao(db.Model):
    __tablename__ = "condicao_habitacao"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    clientes                        = db.relationship("Cliente", back_populates="condicao_habitacao")


class TipoMoradia(db.Model):
    __tablename__ = "tipo_moradia"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    clientes                        = db.relationship("Cliente", back_populates="tipo_moradia")


class TipoTransporte(db.Model):
    __tablename__ = "tipo_transporte"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    clientes                        = db.relationship("Cliente", back_populates="tipo_transporte")


class Escolaridade(db.Model):
    __tablename__ = "escolaridade"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    clientes                        = db.relationship("Cliente", back_populates="escolaridade")


class MetodoPagamento(db.Model):
    __tablename__ = "metodo_pagamento"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    juros                           = db.Column(db.Float, nullable=False, default=0.0)
    guias                           = db.relationship("Guia", back_populates="metodo_pagamento")


class Situacao(db.Model):
    __tablename__ = "situacao"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    encaminhamentos                 = db.relationship("Encaminhamento", back_populates="situacao")


class GrauParentesco(db.Model):
    __tablename__ = "grau_parentesco"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    clientes                        = db.relationship("Cliente", back_populates="grau_parentesco")


class TipoEncaminhamento(db.Model):
    __tablename__ = "tipo_encaminhamento"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    encaminhamento                  = db.relationship("Encaminhamento", back_populates="tipo_encaminhamento")


class EstadosCivis(db.Model):
    __tablename__ = "estados_civis"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    clientes                        = db.relationship("Cliente", back_populates="estado_civil")    

# USUÁRIO


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    email                           = db.Column(db.String(255), unique=True, nullable=False)
    senha                           = db.Column(db.String(255), nullable=False)
    role                            = db.Column(db.String(50), nullable=False)  # 'admin', 'financeiro', 'atendimento'.
    is_active                       = db.Column(db.Boolean, default=True)
    is_authenticated                = db.Column(db.Boolean, default=False)
    is_anonymous                    = db.Column(db.Boolean, default=False)
    data_cadastro                   = db.Column(db.DateTime, default=db.func.current_timestamp())

    guias                           = db.relationship("Guia", back_populates="usuario_emitente", cascade="all, delete-orphan")

    # Flask-Login methods
    def get_id(self):
        return str(self.id)
    
    def is_active(self):
        return self.is_active
    
    def is_authenticated(self):
        return self.is_authenticated

# CLIENTE


class Cliente(db.Model):

    __tablename__ = "clientes"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    cpf                             = db.Column(db.String(14), unique=True, nullable=False)
    email                           = db.Column(db.String(255), nullable=False)
    data_nascimento                 = db.Column(db.DateTime)
    renda_familiar                  = db.Column(db.Float, nullable=False, default=0.0)
    bairro                          = db.Column(db.String(255))
    canal_divulgacao                = db.Column(db.String(255), default="")
    cep                             = db.Column(db.String(10))
    cidade                          = db.Column(db.String(255))
    cpf_responsavel                 = db.Column(db.String(14), unique=True)
    complemento                     = db.Column(db.String(255))
    numero_cs                       = db.Column(db.String(20))
    despesa_mensal                  = db.Column(db.Float, nullable=False, default=0.0)
    estado                          = db.Column(db.String(255))
    endereco                        = db.Column(db.String(255))
    fone_contato                    = db.Column(db.String(20))
    fone_pessoal                    = db.Column(db.String(20))
    nome_plano_saude                = db.Column(db.String(255), default="")
    plano_saude                     = db.Column(db.String(255))
    nome_responsavel                = db.Column(db.String(255))
    possui_filhos                   = db.Column(db.String(255))
    numero_filhos                   = db.Column(db.Integer)
    previdenciario                  = db.Column(db.String(255))
    profissao                       = db.Column(db.String(255), default="")
    remuneracao                     = db.Column(db.Float, nullable=False, default=0.0)
    rg                              = db.Column(db.String(20))
    saldo                           = db.Column(db.Float, nullable=False, default=0.0)
    idade                           = db.Column(db.Integer)
    data_cadastro                   = db.Column(db.DateTime, default=db.func.current_timestamp())
    sexo_id                         = db.Column(db.Integer, db.ForeignKey("sexo.id"))
    condicao_habitacao_id           = db.Column(db.Integer, db.ForeignKey("condicao_habitacao.id"))
    tipo_moradia_id                 = db.Column(db.Integer, db.ForeignKey("tipo_moradia.id"))
    tipo_transporte_id              = db.Column(db.Integer, db.ForeignKey("tipo_transporte.id"))
    escolaridade_id                 = db.Column(db.Integer, db.ForeignKey("escolaridade.id"))
    grau_parentesco_id              = db.Column(db.Integer, db.ForeignKey("grau_parentesco.id"))
    estado_civil_id                 = db.Column(db.Integer, db.ForeignKey("estados_civis.id"))
    estado_civil                    = db.relationship("EstadosCivis", back_populates="clientes")
    sexo                            = db.relationship("Sexo", back_populates="clientes")
    condicao_habitacao              = db.relationship("CondicaoHabitacao", back_populates="clientes")
    tipo_moradia                    = db.relationship("TipoMoradia", back_populates="clientes")
    tipo_transporte                 = db.relationship("TipoTransporte", back_populates="clientes")
    escolaridade                    = db.relationship("Escolaridade", back_populates="clientes")
    grau_parentesco                 = db.relationship("GrauParentesco", back_populates="clientes")
    encaminhamentos                 = db.relationship("Encaminhamento", back_populates="cliente", cascade="all, delete-orphan")
    guias                           = db.relationship("Guia", back_populates="cliente", cascade="all, delete-orphan")


# PROFISSIONAL
class Profissional(db.Model):
    __tablename__ = "profissionais"
    id                              = db.Column(db.Integer, primary_key=True)
    nome                            = db.Column(db.String(255), nullable=False)
    cpf                             = db.Column(db.String(14), unique=True, nullable=False)
    email                           = db.Column(db.String(255))
    data_nascimento                 = db.Column(db.DateTime)
    bairro                          = db.Column(db.String)
    banco                           = db.Column(db.String)
    cep                             = db.Column(db.String)
    cidade                          = db.Column(db.String)
    complemento                     = db.Column(db.String)
    graduacao                       = db.Column(db.String)
    issqn                           = db.Column(db.String)
    fone_pessoal                    = db.Column(db.String)
    fone_profissional               = db.Column(db.String)
    curriculum_lattes               = db.Column(db.String)
    dias_horas_disponiveis          = db.Column(db.String)
    endereco_profissional           = db.Column(db.String)
    estado                          = db.Column(db.String)
    observacoes                     = db.Column(db.String)
    pix                             = db.Column(db.String)
    registro_profissional           = db.Column(db.String)
    rg                              = db.Column(db.String(11), unique=True, nullable=False)
    valor_minimo                    = db.Column(db.Float)
    data_cadastro                   = db.Column(db.DateTime, default=db.func.current_timestamp())

    encaminhamentos                 = db.relationship("Encaminhamento", back_populates="profissional", cascade="all, delete-orphan")
    guias                           = db.relationship("Guia", back_populates="profissional", cascade="all, delete-orphan")


# ENCAMINHAMENTO
class Encaminhamento(db.Model):
    __tablename__ = "encaminhamentos"
    id                              = db.Column(db.Integer, primary_key=True)
    convenio                        = db.Column(db.String)
    dias_horas_atendimento          = db.Column(db.String)
    data_encaminhamento             = db.Column(db.DateTime, default=db.func.current_timestamp())
    observacoes_gerais              = db.Column(db.String)
    queixa                          = db.Column(db.String)
    valor                           = db.Column(db.Float)
    data_cadastro                   = db.Column(db.DateTime, default=db.func.current_timestamp())

    cliente_id                      = db.Column(db.Integer, db.ForeignKey("clientes.id", ondelete="CASCADE"))
    profissional_id                 = db.Column(db.Integer, db.ForeignKey("profissionais.id", ondelete="CASCADE"))
    situacao_id                     = db.Column(db.Integer, db.ForeignKey("situacao.id"))
    tipo_encaminhamento_id          = db.Column(db.Integer, db.ForeignKey("tipo_encaminhamento.id"))

    situacao                        = db.relationship("Situacao", back_populates="encaminhamentos")
    tipo_encaminhamento             = db.relationship("TipoEncaminhamento", back_populates="encaminhamento")
    cliente                         = db.relationship("Cliente", back_populates="encaminhamentos", passive_deletes=True)
    profissional                    = db.relationship("Profissional", back_populates="encaminhamentos", passive_deletes=True)


# GUIA
class Guia(db.Model):
    __tablename__ = "guias"
    id                              = db.Column(db.Integer, primary_key=True)
    cliente_id                      = db.Column(db.Integer, db.ForeignKey("clientes.id", ondelete="CASCADE"))
    profissional_id                 = db.Column(db.Integer, db.ForeignKey("profissionais.id", ondelete="CASCADE"))
    metodo_pagamento_id             = db.Column(db.Integer, db.ForeignKey("metodo_pagamento.id"))
    data_original                   = db.Column(db.DateTime)
    hora_emissao                    = db.Column(db.String(10))
    observacoes_gerais              = db.Column(db.String(500))
    quantidade_emissoes             = db.Column(db.Integer)
    valor_unitario                  = db.Column(db.Float)
    valor_total                     = db.Column(db.Float)
    pago                            = db.Column(db.String(50))
    data_cadastro                   = db.Column(db.DateTime, default=db.func.current_timestamp())
    usuario_emitente_id             = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    
    usuario_emitente = db.relationship("Usuario", back_populates="guias")
    cliente = db.relationship("Cliente", back_populates="guias", passive_deletes=True)
    profissional = db.relationship("Profissional", back_populates="guias", passive_deletes=True)
    metodo_pagamento = db.relationship("MetodoPagamento", back_populates="guias")
