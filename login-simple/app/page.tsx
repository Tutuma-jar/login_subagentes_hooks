const benefits = [
  {
    icon: "✓",
    title: "Todo en un mismo lugar",
    description:
      "Organiza tus credenciales, documentos y avances sin saltar entre herramientas.",
  },
  {
    icon: "↗",
    title: "Avanza con claridad",
    description:
      "Una experiencia simple para saber qué sigue y llegar a tus objetivos.",
  },
  {
    icon: "◌",
    title: "Hecho para crecer",
    description:
      "Una base ágil para equipos y personas que quieren ir más lejos.",
  },
];

export default function Home() {
  return (
    <main className="overflow-hidden bg-[#f8fafc] text-slate-950">
      <section className="relative isolate min-h-[720px] overflow-hidden">
        <div className="absolute inset-x-0 top-0 -z-20 h-[650px] bg-[radial-gradient(circle_at_80%_20%,#c7d2fe_0,transparent_30%),radial-gradient(circle_at_10%_25%,#d1fae5_0,transparent_28%),linear-gradient(125deg,#f8fafc_10%,#eef2ff_52%,#ecfdf5_100%)]" />
        <div className="absolute -right-24 top-36 -z-10 h-80 w-80 rounded-full bg-indigo-300/30 blur-3xl" />
        <div className="absolute -left-20 top-80 -z-10 h-72 w-72 rounded-full bg-emerald-200/40 blur-3xl" />

        <nav className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-6 lg:px-8">
          <a href="#inicio" className="flex items-center gap-2.5 font-semibold tracking-tight">
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-slate-950 text-lg text-white shadow-lg shadow-slate-950/20">
              C
            </span>
            <span className="text-xl">certi</span>
          </a>
          <div className="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
            <a className="transition hover:text-slate-950" href="#como-funciona">
              Cómo funciona
            </a>
            <a className="transition hover:text-slate-950" href="#beneficios">
              Beneficios
            </a>
            <a className="transition hover:text-slate-950" href="#contacto">
              Contacto
            </a>
          </div>
          <a
            href="#empezar"
            className="rounded-full bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-slate-950/15 transition hover:-translate-y-0.5 hover:bg-slate-800"
          >
            Empezar ahora
          </a>
        </nav>

        <div id="inicio" className="mx-auto grid max-w-6xl gap-14 px-6 pb-20 pt-16 lg:grid-cols-[1fr_0.92fr] lg:items-center lg:px-8 lg:pb-28 lg:pt-24">
          <div className="max-w-2xl">
            <p className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-white/70 px-3 py-1.5 text-sm font-semibold text-indigo-700 shadow-sm backdrop-blur">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              Tu próximo paso empieza aquí
            </p>
            <h1 className="text-5xl font-semibold leading-[1.03] tracking-[-0.055em] text-slate-950 sm:text-6xl lg:text-7xl">
              Avanza con la confianza de tenerlo todo claro.
            </h1>
            <p className="mt-7 max-w-xl text-lg leading-8 text-slate-600 sm:text-xl">
              Certi reúne tus procesos, avances y oportunidades en un espacio diseñado para que puedas enfocarte en llegar más lejos.
            </p>
            <div id="empezar" className="mt-9 flex flex-col gap-3 sm:flex-row">
              <a
                href="mailto:hola@certi.com?subject=Quiero%20conocer%20Certi"
                className="rounded-full bg-indigo-600 px-6 py-3.5 text-center text-sm font-semibold text-white shadow-xl shadow-indigo-500/25 transition hover:-translate-y-0.5 hover:bg-indigo-700"
              >
                Quiero conocer Certi
              </a>
              <a
                href="#como-funciona"
                className="rounded-full border border-slate-300 bg-white/75 px-6 py-3.5 text-center text-sm font-semibold text-slate-700 transition hover:border-slate-400 hover:bg-white"
              >
                Ver cómo funciona
              </a>
            </div>
            <div className="mt-10 flex items-center gap-4 text-sm text-slate-500">
              <div className="flex -space-x-2">
                {["AM", "LC", "JR"].map((initials, index) => (
                  <span
                    key={initials}
                    className={`grid h-8 w-8 place-items-center rounded-full border-2 border-white text-[10px] font-bold text-white ${["bg-rose-400", "bg-sky-500", "bg-amber-500"][index]}`}
                  >
                    {initials}
                  </span>
                ))}
              </div>
              Más de 1.200 personas ya están avanzando
            </div>
          </div>

          <div className="relative mx-auto w-full max-w-lg lg:max-w-none">
            <div className="absolute -inset-5 rounded-[2.5rem] bg-white/40 blur-xl" />
            <div className="relative rounded-[2rem] border border-white/90 bg-white/80 p-4 shadow-2xl shadow-indigo-950/10 backdrop-blur sm:p-5">
              <div className="rounded-[1.45rem] bg-slate-950 p-5 text-white sm:p-7">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-medium text-slate-400">Tu espacio</p>
                    <p className="mt-1 text-lg font-semibold">Buenos días, Andrea</p>
                  </div>
                  <span className="grid h-10 w-10 place-items-center rounded-full bg-gradient-to-br from-indigo-400 to-violet-600 text-sm font-bold">
                    A
                  </span>
                </div>
                <div className="mt-7 rounded-2xl bg-white/10 p-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-300">Tu progreso</span>
                    <span className="font-semibold text-emerald-300">78%</span>
                  </div>
                  <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/10">
                    <div className="h-full w-[78%] rounded-full bg-gradient-to-r from-emerald-300 to-teal-400" />
                  </div>
                  <p className="mt-3 text-xs text-slate-400">Estás a un paso de completar tu perfil.</p>
                </div>
              </div>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <div className="rounded-2xl border border-slate-100 bg-white p-4 shadow-sm">
                  <span className="text-xs font-medium text-slate-500">Próximo hito</span>
                  <p className="mt-2 text-sm font-semibold text-slate-900">Revisar tu solicitud</p>
                  <p className="mt-1 text-xs text-indigo-600">Disponible hoy</p>
                </div>
                <div className="rounded-2xl border border-slate-100 bg-emerald-50 p-4">
                  <span className="text-xs font-medium text-emerald-700">Todo al día</span>
                  <p className="mt-2 text-sm font-semibold text-slate-900">3 tareas completadas</p>
                  <p className="mt-1 text-xs text-emerald-700">Sigue así</p>
                </div>
              </div>
            </div>
            <div className="absolute -bottom-6 -left-6 hidden items-center gap-3 rounded-2xl border border-white bg-white px-4 py-3 shadow-xl shadow-slate-900/10 sm:flex">
              <span className="grid h-9 w-9 place-items-center rounded-xl bg-emerald-100 text-lg text-emerald-700">✓</span>
              <div>
                <p className="text-xs font-medium text-slate-500">Nuevo avance</p>
                <p className="text-sm font-semibold text-slate-900">Perfil actualizado</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="como-funciona" className="mx-auto max-w-6xl px-6 py-24 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-sm font-bold uppercase tracking-[0.18em] text-indigo-600">Simple por diseño</p>
          <h2 className="mt-4 text-3xl font-semibold tracking-[-0.04em] text-slate-950 sm:text-5xl">
            Menos fricción. Más foco en lo que importa.
          </h2>
        </div>
        <div id="beneficios" className="mt-12 grid gap-5 md:grid-cols-3">
          {benefits.map((benefit, index) => (
            <article key={benefit.title} className="group rounded-3xl border border-slate-200 bg-white p-7 shadow-sm transition hover:-translate-y-1 hover:shadow-xl hover:shadow-slate-200/60">
              <span className={`grid h-11 w-11 place-items-center rounded-2xl text-lg font-bold ${index === 0 ? "bg-indigo-100 text-indigo-700" : index === 1 ? "bg-amber-100 text-amber-700" : "bg-emerald-100 text-emerald-700"}`}>
                {benefit.icon}
              </span>
              <h3 className="mt-6 text-xl font-semibold tracking-tight text-slate-900">{benefit.title}</h3>
              <p className="mt-3 leading-7 text-slate-600">{benefit.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="contacto" className="px-6 pb-24 lg:px-8">
        <div className="mx-auto max-w-6xl overflow-hidden rounded-[2rem] bg-slate-950 px-7 py-12 text-center text-white sm:px-12 sm:py-16">
          <p className="text-sm font-semibold text-indigo-300">EL MOMENTO ES AHORA</p>
          <h2 className="mx-auto mt-3 max-w-2xl text-3xl font-semibold tracking-[-0.04em] sm:text-5xl">
            Convierte tu próximo paso en una gran oportunidad.
          </h2>
          <p className="mx-auto mt-5 max-w-xl text-slate-300">Conoce una forma más clara y humana de avanzar.</p>
          <a
            href="mailto:hola@certi.com?subject=Quiero%20conocer%20Certi"
            className="mt-8 inline-flex rounded-full bg-white px-6 py-3.5 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5 hover:bg-indigo-100"
          >
            Hablemos
          </a>
        </div>
      </section>

      <footer className="border-t border-slate-200 px-6 py-8 lg:px-8">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 text-sm text-slate-500 sm:flex-row">
          <p>© 2026 Certi. Avanzar también puede ser simple.</p>
          <a className="font-medium text-slate-700 hover:text-indigo-600" href="mailto:hola@certi.com">
            hola@certi.com
          </a>
        </div>
      </footer>
    </main>
  );
}
