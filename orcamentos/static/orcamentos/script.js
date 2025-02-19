function atualizarTotalOrcamento() {
  let total = 0
  $('#itens-orcamento .item-row').each(function () {
    let quantidade = parseFloat($(this).find('.quantidade').val()) || 0
    let precoUnitario = parseFloat($(this).find('.preco-unitario').val()) || 0
    let totalLinha = quantidade * precoUnitario
    $(this).find('.total').val(totalLinha.toFixed(2))
    total += totalLinha
  })
  $('#id_orca_valo_tota').val(total.toFixed(2))
}

$(document).ready(function () {
  var totalForms = $('#id_pecas-TOTAL_FORMS')

  // Evento para campos de busca (autocomplete)
  $(document).on('keyup', '.busca-produto', function () {
    let input = $(this)
    let query = input.val()
    let resultados = input.siblings('.resultado-busca')

    if (query.length < 3) {
      resultados.empty()
      return
    }

    $.ajax({
      url: "{% url 'buscar_produtos' %}",
      data: { term: query },
      dataType: 'json',
      success: function (data) {
        resultados.empty()
        data.forEach(function (produto) {
          resultados.append(`
        <li class="list-group-item list-group-item-action" data-id="${produto.id}" data-nome="${produto.nome}">
          ${produto.nome} (${produto.codigo})
        </li>
      `)
        })
        resultados.show()
      },
    })
  })

  // Evento para selecionar um produto da lista
  $(document).on('click', '.resultado-busca li', function () {
    let produtoId = $(this).data('id')
    let produtoNome = $(this).data('nome')
    let inputBusca = $(this).closest('td').find('.busca-produto')
    let inputId = $(this).closest('td').find('.produto-id')

    inputBusca.val(produtoNome)
    inputId.val(produtoId)
    $(this).closest('.resultado-busca').empty().hide()
  })

  // Esconder a lista de busca ao clicar fora
  $(document).on('click', function (e) {
    if (!$(e.target).closest('.busca-produto, .resultado-busca').length) {
      $('.resultado-busca').empty().hide()
    }
  })

  // Adicionar um novo item
  $('#add-item').click(function () {
    var currentFormCount = parseInt(totalForms.val())
    var newRow = `
  <tr class="item-row">
    <td>
      <input type="text" class="form-control busca-produto" placeholder="Buscar produto..." autocomplete="on">
      <input type="hidden" name="pecas-${currentFormCount}-peca_codi" class="produto-id">
      <ul class="list-group resultado-busca"></ul>
    </td>
    <td>
      <input type="number" name="pecas-${currentFormCount}-peca_quan" class="form-control quantidade" min="1" value="1" required>
    </td>
    <td>
      <input type="text" name="pecas-${currentFormCount}-peca_unit" class="form-control preco-unitario" step="0.01" value="0.00" required>
    </td>
    <td>
      <input type="text" name="pecas-${currentFormCount}-peca_tota" class="form-control total" value="0.00" readonly>
    </td>
    <td>
      <input type="text" name="pecas-${currentFormCount}-peca_comp" class="form-control">
    </td>
    <td>
      <button type="button" class="btn btn-danger remove-item">Remover</button>
    </td>
  </tr>
`
    $('#itens-orcamento').append(newRow)
    totalForms.val(currentFormCount + 1)
    atualizarTotalOrcamento()
  })

  // Remover um item
  $(document).on('click', '.remove-item', function () {
    $(this).closest('tr').remove()
    atualizarTotalOrcamento()
  })

  // Atualizar total ao alterar quantidade ou preço
  $(document).on('input', '.quantidade, .preco-unitario', function () {
    atualizarTotalOrcamento()
  })
})

$(document).ready(function () {
  // Quando o usuário digitar no campo de busca...
  $(document).on('keyup', '.busca-produto', function () {
    var $input = $(this)
    var query = $input.val()
    var $resultados = $input.siblings('.resultado-busca')

    // Se não digitar nada, limpa a lista
    if (query.length === 0) {
      $resultados.empty().hide()
      return
    }

    $.ajax({
      url: "{% url 'buscar_produtos' %}",
      data: { term: query },
      dataType: 'json',
      success: function (data) {
        $resultados.empty()
        if (data.length > 0) {
          $.each(data, function (index, produto) {
            // Cria um item para cada produto retornado
            $resultados.append(
              "<li class='list-group-item list-group-item-action' data-id='" +
                produto.id +
                "' data-nome='" +
                produto.nome +
                "'>" +
                produto.nome +
                ' (' +
                produto.codigo +
                ')' +
                '</li>'
            )
          })
          $resultados.show()
        } else {
          $resultados.hide()
        }
      },
      error: function () {
        $resultados.empty().hide()
      },
    })
  })

  // Quando o usuário clicar em um item da lista...
  $(document).on('click', '.resultado-busca li', function () {
    var $li = $(this)
    var produtoNome = $li.data('nome')
    var produtoId = $li.data('id')
    var $td = $li.closest('td')
    $td.find('.busca-produto').val(produtoNome)
    $td.find('.produto-id').val(produtoId)
    $li.parent().empty().hide()
  })

  // Esconder a lista se clicar fora
  $(document).on('click', function (e) {
    if (!$(e.target).closest('.busca-produto, .resultado-busca').length) {
      $('.resultado-busca').empty().hide()
    }
  })
})

$('#cliente').on('input', function () {
  let query = $(this).val()
  if (query.length > 1) {
    $.ajax({
      url: "{% url 'buscar_clientes' %}",
      data: { term: query }, // Use 'term' aqui
      success: function (data) {
        $('#lista-clientes').empty()
        $.each(data, function (index, cliente) {
          $('#lista-clientes').append(
            `<li class="list-group-item" data-id="${cliente.id}">${cliente.nome}</li>`
          )
        })
      },
    })
  } else {
    $('#lista-clientes').empty()
  }
})

// Ao clicar em um item da lista de clientes
$(document).on('click', '#lista-clientes li', function () {
  let id = $(this).data('id')
  let nome = $(this).text()
  $('#cliente').val(nome) // Atualiza o campo de busca com o nome
  // Atualiza o campo oculto do formulário (pedi_forn)
  $("[name='pedi_forn']").val(id)
  $('#lista-clientes').empty()
})

// Autocomplete para Vendedores
$('#vendedor').on('input', function () {
  let query = $(this).val()
  if (query.length > 1) {
    $.ajax({
      url: "{% url 'buscar_vendedores' %}",
      data: { term: query }, // Use 'term' aqui também
      success: function (data) {
        $('#lista-vendedores').empty()
        $.each(data, function (index, vendedor) {
          $('#lista-vendedores').append(
            `<li class="list-group-item" data-id="${vendedor.id}">${vendedor.nome}</li>`
          )
        })
      },
    })
  } else {
    $('#lista-vendedores').empty()
  }
})

// Ao clicar em um item da lista de vendedores
$(document).on('click', '#lista-vendedores li', function () {
  let id = $(this).data('id')
  let nome = $(this).text()
  $('#vendedor').val(nome) // Atualiza o campo de busca com o nome
  // Atualiza o campo oculto do formulário (pedi_vend)
  $("[name='pedi_vend']").val(id)
  $('#lista-vendedores').empty()
})
