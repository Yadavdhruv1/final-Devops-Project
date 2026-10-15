{{/* Generate common labels */}}
{{- define "finpilot.labels" -}}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

{{/* Backend labels */}}
{{- define "finpilot.backend.labels" -}}
app: finpilot-backend
component: backend
{{ include "finpilot.labels" . }}
{{- end }}

{{/* Frontend labels */}}
{{- define "finpilot.frontend.labels" -}}
app: finpilot-frontend
component: frontend
{{ include "finpilot.labels" . }}
{{- end }}

{{/* PostgreSQL labels */}}
{{- define "finpilot.postgresql.labels" -}}
app: finpilot-postgresql
component: database
{{ include "finpilot.labels" . }}
{{- end }}
