import { useOauthStore } from '@/stores/oauth'
import { navigateTo } from 'nuxt/app'

export default defineNuxtRouteMiddleware((to, from) => {
  const oauthStore = useOauthStore()
  const { tokenInfo } = oauthStore

  // Check if user is authenticated first
  const authenticated = tokenInfo && tokenInfo.access_token && tokenInfo.access_token.length > 0
  const currentTime = Math.floor(Date.now() / 1000)
  const tokenValid = tokenInfo && tokenInfo.exp && tokenInfo.exp > currentTime

  if (!authenticated || !tokenValid) {
    return navigateTo('/login')
  }

  // Define role-based route restrictions
  const roleRestrictions: Record<string, { allowedRoles: string[] }> = {
    // ADMIN ONLY ROUTES
    '/dss/dashboard': {
      allowedRoles: ['admin']
    },
    '/dss/orders': {
      allowedRoles: ['admin']
    },
    '/dss/services': {
      allowedRoles: ['admin']
    },
    '/dss/customers': {
      allowedRoles: ['admin']
    },
    '/dss/users': {
      allowedRoles: ['admin']
    },
    '/dss/tasks': {
      allowedRoles: ['admin']
    },
    '/dss/reports': {
      allowedRoles: ['admin']
    },
    '/dss/settings': {
      allowedRoles: ['admin']
    },
    
    // EMPLOYEE ONLY ROUTES
    '/dss/employee-orders': {
      allowedRoles: ['employee']
    },
    '/dss/employee-tasks': {
      allowedRoles: ['employee']
    },
    '/dss/employee-schedule': {
      allowedRoles: ['employee']
    },
    
    // CUSTOMER ONLY ROUTES
    '/dss/customer-orders': {
      allowedRoles: ['customer']
    },
    '/dss/customer-bookings': {
      allowedRoles: ['customer']
    },
    
    // SHARED ROUTES (all authenticated users)
    '/dss/profile': {
      allowedRoles: ['admin', 'employee', 'customer']
    },
    '/dss/notifications': {
      allowedRoles: ['admin', 'employee', 'customer']
    }
  }

  // Get user role
  const userRole = getUserRole(tokenInfo)
  console.log('=== MIDDLEWARE DEBUG ===')
  console.log('User role:', userRole, 'Path:', to.path)
  console.log('Token info:', { isStaff: tokenInfo?.isStaff, isSuperuser: tokenInfo?.isSuperuser, scope: tokenInfo?.scope })
  
  // Check if current path has restrictions
  const currentPathRestriction = Object.keys(roleRestrictions).find(path => 
    to.path.startsWith(path)
  )
  
  console.log('Found restriction for path:', currentPathRestriction)

  if (currentPathRestriction) {
    const restriction = roleRestrictions[currentPathRestriction]
    
    // Check role permission
    if (!restriction.allowedRoles.includes(userRole)) {
      console.log(`Access denied for role ${userRole} to path ${to.path}`)
      
      // Redirect to access denied page
      return navigateTo('/access-denied')
    }
  } else if (to.path.startsWith('/dss/')) {
    // For any /dss/* route not explicitly defined, default to admin only
    if (userRole !== 'admin') {
      console.log(`Access denied for role ${userRole} to undefined path ${to.path} - defaulting to admin only`)
      
      // Redirect to access denied page
      return navigateTo('/access-denied')
    }
  }
})

function getUserRole(tokenInfo: any): string {
  console.log('=== GET USER ROLE DEBUG ===')
  console.log('tokenInfo:', tokenInfo)
  
  if (!tokenInfo) {
    console.log('No token info, returning guest')
    return 'guest'
  }
  
  // Check if user is admin/superuser
  if (tokenInfo.isSuperuser) {
    console.log('User is superuser (admin)')
    return 'admin'
  }
  
  // Check if user is staff (employee)
  if (tokenInfo.isStaff) {
    console.log('User is staff (employee)')
    return 'employee'
  }
  
  // Check scopes to determine if employee (backup check)
  const scope = tokenInfo.scope || ''
  const scopes = scope.split(' ')
  console.log('Scopes:', scopes)
  
  // If has employee scope, consider as employee
  if (scopes.includes('employees:view')) {
    console.log('User has employees:view scope, returning employee')
    return 'employee'
  }
  
  // Check if guest
  if (tokenInfo.isGuest) {
    console.log('User is guest')
    return 'guest'
  }
  
  // Default to customer
  console.log('Defaulting to customer')
  return 'customer'
}