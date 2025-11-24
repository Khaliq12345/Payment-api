export default defineNuxtRouteMiddleware((to, from) => {
  // On ignore côté serveur car localStorage n'existe pas
  if (import.meta.server) return

  const user = localStorage.getItem('user')
  const expiredAt = localStorage.getItem('expired_at')

  // Si pas d'utilisateur ou pas de date d'expiration, on redirige
  if (!user || !expiredAt) return navigateTo('/login')

  // Vérification de l'expiration
  if (new Date() > new Date(expiredAt)) {
    
    // Session expirée 
    localStorage.removeItem('user')
    localStorage.removeItem('expired_at')
    return navigateTo('/login')
  }
})
