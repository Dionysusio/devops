import Cookies from 'js-cookie'
import store from '../store'

const TokenKey = 'friedrich-token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

// 验证权限
export function checkPermission(perm) { // perm 传的权限
  if (store.getters.permission.indexOf(perm) > -1) { // 大于-1 就是找到了
    return true
  }
  return false
}

export function checkPerms(perm) {
  if (store.getters.permission.indexOf(perm) > -1) {
    return true
  }
  return false
}
