"""
Script para poblar la base de datos con datos iniciales.

Ejecutar con: python -m scripts.seed_data
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models.institution import Institution
from src.models.program import Program
from src.models.trajectory import Trajectory


def create_institutions(db: Session) -> dict[str, Institution]:
    """Crea instituciones educativas de Argentina."""
    institutions_data = [
        {
            "name": "Universidad de Buenos Aires",
            "short_name": "UBA",
            "type": "university",
            "province": "Buenos Aires",
            "city": "Ciudad Autónoma de Buenos Aires",
            "website": "https://www.uba.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Tecnológica Nacional",
            "short_name": "UTN",
            "type": "university",
            "province": "Buenos Aires",
            "city": "Ciudad Autónoma de Buenos Aires",
            "website": "https://www.utn.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de La Plata",
            "short_name": "UNLP",
            "type": "university",
            "province": "Buenos Aires",
            "city": "La Plata",
            "website": "https://unlp.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de Córdoba",
            "short_name": "UNC",
            "type": "university",
            "province": "Córdoba",
            "city": "Córdoba",
            "website": "https://www.unc.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de Rosario",
            "short_name": "UNR",
            "type": "university",
            "province": "Santa Fe",
            "city": "Rosario",
            "website": "https://www.unr.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de Cuyo",
            "short_name": "UNCuyo",
            "type": "university",
            "province": "Mendoza",
            "city": "Mendoza",
            "website": "https://www.uncuyo.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional del Litoral",
            "short_name": "UNL",
            "type": "university",
            "province": "Santa Fe",
            "city": "Santa Fe",
            "website": "https://www.unl.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de Tucumán",
            "short_name": "UNT",
            "type": "university",
            "province": "Tucumán",
            "city": "San Miguel de Tucumán",
            "website": "https://www.unt.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de Mar del Plata",
            "short_name": "UNMdP",
            "type": "university",
            "province": "Buenos Aires",
            "city": "Mar del Plata",
            "website": "https://www.mdp.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de San Martín",
            "short_name": "UNSAM",
            "type": "university",
            "province": "Buenos Aires",
            "city": "San Martín",
            "website": "https://www.unsam.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de Quilmes",
            "short_name": "UNQ",
            "type": "university",
            "province": "Buenos Aires",
            "city": "Quilmes",
            "website": "https://www.unq.edu.ar",
            "is_public": True,
        },
        {
            "name": "Universidad Nacional de Tres de Febrero",
            "short_name": "UNTREF",
            "type": "university",
            "province": "Buenos Aires",
            "city": "Caseros",
            "website": "https://www.untref.edu.ar",
            "is_public": True,
        },
        {
            "name": "Instituto Superior de Formación Docente N°1",
            "short_name": "ISFD1",
            "type": "institute",
            "province": "Buenos Aires",
            "city": "Avellaneda",
            "is_public": True,
        },
        {
            "name": "Instituto Tecnológico Buenos Aires",
            "short_name": "ITBA",
            "type": "university",
            "province": "Buenos Aires",
            "city": "Ciudad Autónoma de Buenos Aires",
            "website": "https://www.itba.edu.ar",
            "is_public": False,
        },
    ]

    institutions = {}
    for data in institutions_data:
        inst = Institution(**data)
        db.add(inst)
        db.flush()
        institutions[data["short_name"]] = inst

    return institutions


def create_programs(db: Session, institutions: dict[str, Institution]) -> list[Program]:
    """Crea programas educativos."""
    programs_data = [
        # UBA - Exactas
        {
            "institution": "UBA",
            "name": "Licenciatura en Ciencias de la Computación",
            "type": "degree",
            "duration_years": 5.5,
            "modality": "in_person",
            "weekly_hours": 30,
            "shift": "morning",
            "area": "technology",
            "work_compatible": False,
            "description": "Formación en fundamentos teóricos y prácticos de la computación.",
        },
        {
            "institution": "UBA",
            "name": "Licenciatura en Sistemas de Información",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 25,
            "shift": "evening",
            "area": "technology",
            "work_compatible": True,
            "description": "Carrera orientada a sistemas de información empresarial.",
        },
        {
            "institution": "UBA",
            "name": "Medicina",
            "type": "degree",
            "duration_years": 6,
            "modality": "in_person",
            "weekly_hours": 40,
            "shift": "morning",
            "area": "health",
            "work_compatible": False,
            "description": "Formación médica integral con práctica hospitalaria.",
        },
        {
            "institution": "UBA",
            "name": "Abogacía",
            "type": "degree",
            "duration_years": 5.5,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "flexible",
            "area": "law",
            "work_compatible": True,
            "description": "Formación en derecho con orientación práctica.",
        },
        {
            "institution": "UBA",
            "name": "Contador Público",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 25,
            "shift": "evening",
            "area": "business",
            "work_compatible": True,
            "description": "Carrera en contabilidad y finanzas.",
        },
        {
            "institution": "UBA",
            "name": "Psicología",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "flexible",
            "area": "social_sciences",
            "work_compatible": True,
            "description": "Formación en psicología clínica y social.",
        },
        # UTN
        {
            "institution": "UTN",
            "name": "Ingeniería en Sistemas de Información",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 25,
            "shift": "evening",
            "area": "technology",
            "work_compatible": True,
            "description": "Ingeniería orientada a desarrollo de software y sistemas.",
        },
        {
            "institution": "UTN",
            "name": "Ingeniería Electrónica",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 30,
            "shift": "evening",
            "area": "engineering",
            "work_compatible": True,
            "description": "Diseño y desarrollo de sistemas electrónicos.",
        },
        {
            "institution": "UTN",
            "name": "Ingeniería Mecánica",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 30,
            "shift": "evening",
            "area": "engineering",
            "work_compatible": True,
            "description": "Diseño y producción de sistemas mecánicos.",
        },
        {
            "institution": "UTN",
            "name": "Tecnicatura Universitaria en Programación",
            "type": "technical",
            "duration_years": 2,
            "modality": "hybrid",
            "weekly_hours": 20,
            "shift": "evening",
            "area": "technology",
            "work_compatible": True,
            "description": "Formación práctica en desarrollo de software.",
        },
        # UNLP
        {
            "institution": "UNLP",
            "name": "Licenciatura en Informática",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 25,
            "shift": "morning",
            "area": "technology",
            "work_compatible": False,
            "description": "Formación integral en informática y computación.",
        },
        {
            "institution": "UNLP",
            "name": "Analista Programador Universitario",
            "type": "technical",
            "duration_years": 3,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "evening",
            "area": "technology",
            "work_compatible": True,
            "description": "Título intermedio orientado a programación.",
        },
        {
            "institution": "UNLP",
            "name": "Diseño en Comunicación Visual",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 25,
            "shift": "morning",
            "area": "arts",
            "work_compatible": False,
            "description": "Formación en diseño gráfico y comunicación visual.",
        },
        # UNC
        {
            "institution": "UNC",
            "name": "Ingeniería en Computación",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 30,
            "shift": "morning",
            "area": "technology",
            "work_compatible": False,
            "description": "Ingeniería orientada a hardware y software.",
        },
        {
            "institution": "UNC",
            "name": "Ciencias de la Educación",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "flexible",
            "area": "education",
            "work_compatible": True,
            "description": "Formación en pedagogía y gestión educativa.",
        },
        {
            "institution": "UNC",
            "name": "Arquitectura",
            "type": "degree",
            "duration_years": 6,
            "modality": "in_person",
            "weekly_hours": 35,
            "shift": "morning",
            "area": "arts",
            "work_compatible": False,
            "description": "Diseño arquitectónico y urbanismo.",
        },
        # UNR
        {
            "institution": "UNR",
            "name": "Licenciatura en Comunicación Social",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "morning",
            "area": "communication",
            "work_compatible": True,
            "description": "Formación en medios y comunicación.",
        },
        {
            "institution": "UNR",
            "name": "Enfermería Universitaria",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 30,
            "shift": "morning",
            "area": "health",
            "work_compatible": False,
            "description": "Formación en cuidados de enfermería.",
        },
        # UNQ - Virtual
        {
            "institution": "UNQ",
            "name": "Licenciatura en Educación",
            "type": "degree",
            "duration_years": 4,
            "modality": "remote",
            "weekly_hours": 15,
            "shift": "flexible",
            "area": "education",
            "work_compatible": True,
            "description": "Carrera virtual para docentes en ejercicio.",
        },
        {
            "institution": "UNQ",
            "name": "Tecnicatura Universitaria en Ciencias Empresariales",
            "type": "technical",
            "duration_years": 2.5,
            "modality": "remote",
            "weekly_hours": 15,
            "shift": "flexible",
            "area": "business",
            "work_compatible": True,
            "description": "Formación en gestión empresarial modalidad virtual.",
        },
        # UNSAM
        {
            "institution": "UNSAM",
            "name": "Licenciatura en Biotecnología",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 35,
            "shift": "morning",
            "area": "exact_sciences",
            "work_compatible": False,
            "description": "Formación en biotecnología y biología molecular.",
        },
        {
            "institution": "UNSAM",
            "name": "Licenciatura en Artes Electrónicas",
            "type": "degree",
            "duration_years": 4,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "afternoon",
            "area": "arts",
            "work_compatible": True,
            "description": "Arte digital, multimedia e instalaciones.",
        },
        # UNTREF
        {
            "institution": "UNTREF",
            "name": "Licenciatura en Artes Electrónicas",
            "type": "degree",
            "duration_years": 4,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "evening",
            "area": "arts",
            "work_compatible": True,
            "description": "Formación en arte y tecnología.",
        },
        {
            "institution": "UNTREF",
            "name": "Ingeniería en Sonido",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 25,
            "shift": "evening",
            "area": "engineering",
            "work_compatible": True,
            "description": "Ingeniería de audio y acústica.",
        },
        # Tecnicaturas cortas
        {
            "institution": "UTN",
            "name": "Tecnicatura en Redes y Telecomunicaciones",
            "type": "technical",
            "duration_years": 2,
            "modality": "hybrid",
            "weekly_hours": 18,
            "shift": "evening",
            "area": "technology",
            "work_compatible": True,
            "description": "Administración de redes y telecomunicaciones.",
        },
        {
            "institution": "UTN",
            "name": "Tecnicatura en Desarrollo Web",
            "type": "technical",
            "duration_years": 2,
            "modality": "remote",
            "weekly_hours": 15,
            "shift": "flexible",
            "area": "technology",
            "work_compatible": True,
            "description": "Desarrollo de aplicaciones web modernas.",
        },
        # UNCuyo
        {
            "institution": "UNCuyo",
            "name": "Ingeniería Agronómica",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 30,
            "shift": "morning",
            "area": "agriculture",
            "work_compatible": False,
            "description": "Producción agrícola y manejo de cultivos.",
        },
        {
            "institution": "UNCuyo",
            "name": "Licenciatura en Enología",
            "type": "degree",
            "duration_years": 5,
            "modality": "in_person",
            "weekly_hours": 25,
            "shift": "morning",
            "area": "agriculture",
            "work_compatible": False,
            "description": "Producción vitivinícola.",
        },
        # ISFD - Formación docente
        {
            "institution": "ISFD1",
            "name": "Profesorado de Educación Primaria",
            "type": "degree",
            "duration_years": 4,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "morning",
            "area": "education",
            "work_compatible": True,
            "description": "Formación docente para nivel primario.",
        },
        {
            "institution": "ISFD1",
            "name": "Profesorado de Educación Inicial",
            "type": "degree",
            "duration_years": 4,
            "modality": "in_person",
            "weekly_hours": 20,
            "shift": "afternoon",
            "area": "education",
            "work_compatible": True,
            "description": "Formación docente para jardín de infantes.",
        },
    ]

    programs = []
    for data in programs_data:
        inst_key = data.pop("institution")
        program = Program(institution_id=institutions[inst_key].id, **data)
        db.add(program)
        programs.append(program)

    db.flush()
    return programs


def create_trajectories(db: Session, programs: list[Program]) -> list[Trajectory]:
    """Crea trayectorias de ejemplo."""
    # Buscar algunos programas específicos
    prog_by_name = {p.name: p for p in programs}

    trajectories_data = [
        {
            "program_name": "Tecnicatura Universitaria en Programación",
            "title": "De trabajar en un call center a programador en 2 años",
            "summary": "Trabajaba en atención al cliente y estudié programación de noche. Hoy trabajo remoto como desarrollador.",
            "story": """Cuando terminé el secundario no tenía idea de qué estudiar. Empecé a trabajar en un call center para ayudar en casa. Después de dos años atendiendo reclamos, me di cuenta que quería algo más.

Un compañero me contó de la Tecnicatura en Programación de la UTN. Lo que me convenció fue que era corta (2 años) y que podía cursarla de noche.

Los primeros meses fueron durísimos. Trabajaba de 9 a 18, y cursaba de 19 a 23. Llegaba a casa destruido. Pero el contenido me enganchó enseguida.

La clave fue encontrar un grupo de estudio. Nos juntábamos los sábados a hacer los TPs. También usé mucho YouTube y freeCodeCamp para reforzar.

A mitad de segundo año conseguí mi primer trabajo como desarrollador Jr. El sueldo era similar al call center, pero el trabajo era otro mundo. Hoy, dos años después de recibirme, trabajo remoto para una empresa de USA.""",
            "challenges": "Lo más difícil fue manejar el cansancio de trabajar y estudiar. También tuve que aprender a estudiar solo, porque en el secundario me llevaban de la mano.",
            "alternatives": "Miré la carrera de Analista de Sistemas, pero eran 3 años y preferí algo más corto para empezar.",
            "outcome": "completed",
            "tags": ["worked_full_time", "career_change", "first_generation"],
            "context": {
                "worked_while_studying": True,
                "province": "Buenos Aires",
                "modality": "hybrid",
                "had_technical_degree": False,
            },
            "year_started": 2022,
            "is_verified": True,
        },
        {
            "program_name": "Ingeniería en Sistemas de Información",
            "title": "Empecé Ingeniería en Sistemas sin saber programar",
            "summary": "Me metí a ingeniería por la salida laboral, sin experiencia previa. Costó, pero se puede.",
            "story": """En el secundario nunca toqué una computadora más que para juegos y redes sociales. Elegí Sistemas porque todos decían que había mucho trabajo.

El primer año fue un shock. Mis compañeros que venían de escuelas técnicas ya sabían programar. Yo no entendía nada de Algoritmos.

Tuve que aprender a pedir ayuda. Los ayudantes de cátedra son clave, no tengan vergüenza de ir a consultarlos. También hay muchos videos en YouTube que explican mejor que algunos profesores.

Lo que me salvó fue ir a cursar siempre. Aunque no entendiera, estar presente ayuda. Y juntarme con compañeros que estaban en la misma que yo.

La UTN tiene turno noche, así que desde tercer año empecé a trabajar de mañana. Al principio eran pasantías, después quedé efectivo. Hoy curso las últimas materias mientras laburo como desarrollador senior.""",
            "challenges": "El CBC de matemática me costó un montón. Lo recursé. También física. No hay que frustrarse si te pasa.",
            "alternatives": "Pensé en cambiarme a la Tecnicatura cuando estaba trabado, pero decidí seguir. Cada uno sabe qué es mejor para su situación.",
            "outcome": "in_progress",
            "tags": ["first_generation", "worked_full_time"],
            "context": {
                "worked_while_studying": True,
                "province": "Buenos Aires",
                "modality": "in_person",
            },
            "year_started": 2019,
            "is_verified": True,
        },
        {
            "program_name": "Medicina",
            "title": "De querer ser médico a encontrarme en enfermería",
            "summary": "Empecé Medicina pero la exigencia me superó. En Enfermería encontré mi vocación real.",
            "story": """Siempre quise ser médico. Era mi sueño de chico, y mi familia me apoyaba. Entré a la UBA con mucha ilusión.

El CBC fue intenso pero lo pasé. Cuando entré a la carrera, todo cambió. Las guardias, la cantidad de horas, el estrés. No dormía, no tenía vida. En segundo año empecé a tener ataques de ansiedad.

Un amigo me sugirió que mirara Enfermería. Al principio me pareció que era "menos", pero fui a una charla y me di cuenta que era exactamente lo que quería: estar cerca de los pacientes, cuidar, pero sin la carga de ser el que toma todas las decisiones.

El cambio fue difícil de aceptar. Sentía que estaba decepcionando a mi familia. Pero cuando empecé a cursar Enfermería, sentí que había encontrado mi lugar. Hoy trabajo en un hospital y amo lo que hago.""",
            "challenges": "Lo más difícil fue aceptar que mi primer sueño no era para mí. También explicarle a mi familia que no era un fracaso.",
            "alternatives": "También miré kinesiología y nutrición antes de decidirme por enfermería.",
            "outcome": "switched",
            "tags": ["career_change", "first_generation"],
            "context": {
                "worked_while_studying": False,
                "province": "Buenos Aires",
                "modality": "in_person",
            },
            "year_started": 2020,
            "is_verified": True,
        },
        {
            "program_name": "Licenciatura en Educación",
            "title": "Estudié a distancia mientras trabajaba de maestra",
            "summary": "Ya era docente pero necesitaba el título universitario. La modalidad virtual fue perfecta para mi situación.",
            "story": """Me recibí de maestra en un terciario a los 22. Trabajé 10 años en escuelas primarias. Pero para ascender a cargos directivos, necesitaba título universitario.

Con dos hijos y trabajo full-time, era imposible cursar presencial. Descubrí que la Universidad de Quilmes tenía la Licenciatura en Educación virtual.

Al principio desconfiaba de estudiar por internet. Pero la plataforma está muy bien armada. Tenés videos, foros, tutores que responden rápido. El material es de calidad.

Lo que más me costó fue organizarme. Estudiaba de noche cuando los chicos dormían, y los fines de semana. Mi marido me bancó mucho.

Lo bueno es que muchos trabajos prácticos los podía relacionar con mi trabajo real. Fue como profesionalizarme mientras seguía enseñando.""",
            "challenges": "Mantener la constancia cuando nadie te obliga. A veces pasaba semanas sin tocar el material.",
            "alternatives": "También miré la UNTREF que tiene algo similar, pero Quilmes tenía mejor reputación en educación.",
            "outcome": "completed",
            "tags": ["remote_learning", "worked_full_time"],
            "context": {
                "worked_while_studying": True,
                "province": "Buenos Aires",
                "modality": "remote",
            },
            "year_started": 2021,
            "is_verified": True,
        },
        {
            "program_name": "Diseño en Comunicación Visual",
            "title": "Elegí diseño aunque todos me decían que no había trabajo",
            "summary": "Seguí mi pasión por el diseño a pesar de los comentarios. Hoy trabajo freelance y me va bien.",
            "story": """Desde chica dibujaba todo el tiempo. Cuando dije que quería estudiar diseño, mi papá me dijo que era perder el tiempo. Que estudie algo 'serio'.

Me anoté igual en la UNLP. Los primeros años fueron increíbles. Por fin estaba aprendiendo algo que me apasionaba de verdad.

En tercer año empecé a hacer trabajos freelance. Logotipos, flyers, después sitios web. Cuando me recibí ya tenía una cartera de clientes.

Hoy trabajo independiente. No es fácil, hay que buscarse los clientes y a veces hay meses flojos. Pero no me arrepiento para nada. Hago lo que me gusta y vivo de eso.

La facultad me dio las bases técnicas, pero lo que más aprendí fue a recibir críticas y a trabajar bajo presión.""",
            "challenges": "Convencer a mi familia. También aprender a cobrar mi trabajo, al principio regalaba todo.",
            "alternatives": "También me gustaba fotografía, pero diseño me pareció más versátil.",
            "outcome": "completed",
            "tags": ["first_generation"],
            "context": {
                "worked_while_studying": True,
                "province": "Buenos Aires",
                "modality": "in_person",
            },
            "year_started": 2018,
            "is_verified": True,
        },
        {
            "program_name": "Contador Público",
            "title": "Estudié Contador para tener un trabajo seguro",
            "summary": "No era mi pasión pero necesitaba estabilidad. Hoy trabajo en un estudio contable y estoy tranquilo.",
            "story": """No tenía una vocación clara. Me gustaban los números y necesitaba una carrera con salida laboral. Elegí Contador Público en la UBA porque era gratis y reconocida.

La carrera es larga y hay materias densas, pero no es imposible. Lo bueno es que desde tercer año podés conseguir trabajo como auxiliar contable.

Conseguí trabajo en un estudio contable mientras cursaba. Empecé ordenando papeles, después fui tomando más responsabilidades. Cuando me recibí, quedé como contador junior.

¿Me apasiona? No especialmente. Pero me permite vivir bien, tengo horarios razonables y trabajo estable. A veces pienso que podría haber estudiado otra cosa, pero no me arrepiento.""",
            "challenges": "Las materias de matemática financiera me costaron. Tuve que ir a profesores particulares.",
            "alternatives": "También pensé en Administración de Empresas, pero Contador tiene más salida laboral.",
            "outcome": "completed",
            "tags": ["worked_full_time"],
            "context": {
                "worked_while_studying": True,
                "province": "Buenos Aires",
                "modality": "in_person",
            },
            "year_started": 2017,
            "is_verified": True,
        },
        {
            "program_name": "Profesorado de Educación Primaria",
            "title": "Siempre supe que quería ser maestra",
            "summary": "Desde chica jugaba a la maestra. Hoy trabajo en lo que amo.",
            "story": """No tuve dudas nunca. Quería ser maestra como mi mamá. Me anoté en el profesorado apenas terminé el secundario.

La carrera dura 4 años y tiene mucha práctica. Desde segundo año ya vas a escuelas a observar y después a dar clases.

Lo que más me gusta es la relación con los chicos. Ver cómo aprenden, cómo crecen. Los primeros días de práctica estaba muerta de nervios, pero después le agarrás la mano.

El sueldo no es mucho, eso es verdad. Pero tenés vacaciones, obra social, y es un trabajo estable. Además, si querés ganar más podés dar clases particulares o trabajar en dos escuelas.""",
            "challenges": "Las planificaciones de clase al principio me llevaban horas. Con el tiempo te hacés más rápida.",
            "alternatives": "Nunca pensé en otra cosa.",
            "outcome": "completed",
            "tags": ["first_generation"],
            "context": {
                "worked_while_studying": False,
                "province": "Buenos Aires",
                "modality": "in_person",
            },
            "year_started": 2019,
            "is_verified": True,
        },
        {
            "program_name": "Ingeniería en Computación",
            "title": "Me mudé de provincia para estudiar",
            "summary": "Dejé mi pueblo en Chaco para estudiar en Córdoba. Fue difícil pero valió la pena.",
            "story": """Soy de un pueblo chico de Chaco. La universidad más cercana estaba a 4 horas. Cuando decidí estudiar Ingeniería en Computación, sabía que tenía que irme.

Me mudé a Córdoba a los 18, sin conocer a nadie. Los primeros meses fueron muy duros. Extrañaba a mi familia, no tenía amigos, y encima las materias eran difíciles.

Lo que me salvó fue el centro de estudiantes. Organizaban juntadas para los de afuera y ahí conocí gente en la misma situación. También descubrí las becas de comedor y transporte que ayudan mucho.

Tardé un par de años más que el plan de estudios, pero me recibí. Hoy trabajo en una empresa de Córdoba y mi familia está orgullosa.""",
            "challenges": "Vivir solo por primera vez, manejar la plata, cocinar. Aprendí de todo.",
            "alternatives": "Podría haber estudiado algo en Resistencia, pero la UNC tiene mejor nivel en computación.",
            "outcome": "completed",
            "tags": ["moved_cities", "first_generation", "scholarship"],
            "context": {
                "worked_while_studying": False,
                "province": "Córdoba",
                "modality": "in_person",
            },
            "year_started": 2017,
            "is_verified": True,
        },
    ]

    trajectories = []
    for data in trajectories_data:
        prog_name = data.pop("program_name")
        program = prog_by_name.get(prog_name)
        trajectory = Trajectory(
            program_id=program.id if program else None,
            **data,
        )
        db.add(trajectory)
        trajectories.append(trajectory)

    db.flush()
    return trajectories


def seed_database():
    """Ejecuta el seed completo."""
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        existing = db.query(Institution).first()
        if existing:
            print("La base de datos ya tiene datos. Saltando seed.")
            return

        print("Poblando base de datos...")

        print("  Creando instituciones...")
        institutions = create_institutions(db)
        print(f"    ✓ {len(institutions)} instituciones creadas")

        print("  Creando programas...")
        programs = create_programs(db, institutions)
        print(f"    ✓ {len(programs)} programas creados")

        print("  Creando trayectorias...")
        trajectories = create_trajectories(db, programs)
        print(f"    ✓ {len(trajectories)} trayectorias creadas")

        db.commit()
        print("\n✅ Seed completado exitosamente!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante el seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
