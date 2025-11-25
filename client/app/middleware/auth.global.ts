export default defineNuxtRouteMiddleware((to, from) => {
  // Ce middleware ne doit s'exécuter que côté client (pour les accès à localStorage).
  if (import.meta.server) return

  const path = to.path || to.fullPath || ''
  
  // On récupère les informations de session
  const user = localStorage.getItem('user')
  const expiredAt = localStorage.getItem('expired_at')

  const now = new Date()
  let isAuthenticated = false
  
  // On vérifie si la session est toujours valide et n'a pas expiré.
  if (user && expiredAt) {
    const exp = new Date(expiredAt)

    if (!isNaN(exp.getTime()) && now <= exp) {
      isAuthenticated = true
    } else {
      // Session expirée
      localStorage.removeItem('user')
      localStorage.removeItem('expired_at')
    }
  }

  
  // Si l'utilisateur est déjà connecté et tente d'accéder à la page de connexion, 
  // on le redirige directement vers le tableau de bord admin.
  if (path === '/login') {
    if (isAuthenticated) {
      return navigateTo('/admin/groups')
    }
    return 
  }

  // Toute route commençant par /admin  est protégée.
  if (path.startsWith('/admin')) {
    if (!isAuthenticated) {
      return navigateTo('/login')
    }
    return 
  }

  // Pour toutes les autres routes
  return
})