from django.core.exceptions import ValidationError

class LicenseMixin:
    def get_license(self):
        # Obtém a licença do usuário autenticado
        return self.request.user.licenca

    def form_valid(self, form):
        # Validar se o usuário tem uma licença associada
        licenca = self.get_license()
        if not licenca:
            raise ValidationError("Usuário não tem licença associada.")
        
        # Definir a licença no formulário antes de salvar
        form.instance.licenca = licenca
        return super().form_valid(form)
