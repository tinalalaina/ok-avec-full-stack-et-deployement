import { AxiosError } from 'axios'
import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import Card from '../components/Card'
import FormField from '../components/FormField'
import { register } from '../api/userService'

const Register = () => {
  const navigate = useNavigate()
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [passwordConfirm, setPasswordConfirm] = useState('')
  const [role, setRole] = useState('CLIENT')
  const [message, setMessage] = useState<string | null>(null)

  const handleRegister = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setMessage(null)
    try {
      await register({
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        password_confirm: passwordConfirm,
        role,
      })
      navigate('/login')
    } catch (error) {
      const apiError = error as AxiosError<Record<string, string[] | string>>
      const data = apiError.response?.data

      const priorityFields = ['detail', 'email', 'password', 'password_confirm', 'role']
      let detail: string | undefined

      for (const field of priorityFields) {
        const value = data?.[field]
        if (typeof value === 'string' && value.trim()) {
          detail = value
          break
        }
        if (Array.isArray(value) && typeof value[0] === 'string' && value[0].trim()) {
          detail = value[0]
          break
        }
      }

      if (!detail && data) {
        const firstError = Object.values(data).find(
          (value) =>
            (typeof value === 'string' && value.trim().length > 0) ||
            (Array.isArray(value) && typeof value[0] === 'string' && value[0].trim().length > 0),
        )

        if (typeof firstError === 'string') {
          detail = firstError
        } else if (Array.isArray(firstError) && typeof firstError[0] === 'string') {
          detail = firstError[0]
        }
      }

      setMessage(detail || 'Inscription échouée. Merci de réessayer.')
    }
  }

  return (
    <div className="page-grid">
      <Card title="Inscription">
        <form onSubmit={handleRegister} className="form-grid">
          <FormField label="Prénom" htmlFor="register-first-name">
            <input
              id="register-first-name"
              type="text"
              value={firstName}
              onChange={(event) => setFirstName(event.target.value)}
              required
            />
          </FormField>
          <FormField label="Nom" htmlFor="register-last-name">
            <input
              id="register-last-name"
              type="text"
              value={lastName}
              onChange={(event) => setLastName(event.target.value)}
              required
            />
          </FormField>
          <FormField label="Email" htmlFor="register-email">
            <input
              id="register-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </FormField>
          <FormField label="Mot de passe" htmlFor="register-password">
            <input
              id="register-password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </FormField>
          <FormField label="Confirmer le mot de passe" htmlFor="register-password-confirm">
            <input
              id="register-password-confirm"
              type="password"
              value={passwordConfirm}
              onChange={(event) => setPasswordConfirm(event.target.value)}
              required
            />
          </FormField>
          <FormField label="Rôle" htmlFor="register-role">
            <select id="register-role" value={role} onChange={(event) => setRole(event.target.value)}>
              <option value="CLIENT">Client</option>
              <option value="PRESTATAIRE">Prestataire</option>
              <option value="ADMIN">Admin</option>
            </select>
          </FormField>
          {message ? <div className="alert">{message}</div> : null}
          <button className="button button-primary" type="submit">
            Créer mon compte
          </button>
        </form>
      </Card>
    </div>
  )
}

export default Register
