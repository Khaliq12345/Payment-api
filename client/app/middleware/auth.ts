export default defineNuxtRouteMiddleware((to, from) => {
  // On ignore côté serveur car localStorage n'existe pas
  if (import.meta.server) return

  const user = localStorage.getItem('user')

  // Si pas d'utilisateur connecté, on redirige vers la page de connexion
  if (!user) return navigateTo('/login')

  try {
    const { expire_at } = JSON.parse(user)

    // Vérification de l'expiration de la session
    if (new Date() > new Date(expire_at)) {
      localStorage.removeItem('user')
      return navigateTo('/login')
    }
  } catch (e) {
    // En cas d'erreur de lecture, on nettoie et on redirige
    localStorage.removeItem('user')
    return navigateTo('/login')
  }
})
