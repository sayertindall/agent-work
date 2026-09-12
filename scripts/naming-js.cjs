#!/usr/bin/env node
// Parse supplied Git blob bytes; never execute project code.
const fs = require('node:fs');
const ts = require('typescript');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const source = ts.createSourceFile(input.path, input.text, ts.ScriptTarget.Latest, true);
if (source.parseDiagnostics.length) {
  throw new Error(ts.flattenDiagnosticMessageText(source.parseDiagnostics[0].messageText, '\n'));
}
const names = [];
const resources = new Set(input.resourceFields);
const isResource = name => typeof name === 'string' && resources.has(name.replace(/([a-z])([A-Z])/g, '$1_$2').toLowerCase());
function record(kind, name, node) {
  const line = source.getLineAndCharacterOfPosition(node.getStart(source)).line + 1;
  names.push([kind, name, line]);
}
function literal(node) {
  return node && (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node));
}
function propertyName(node) {
  if (!node) return undefined;
  if (ts.isIdentifier(node) || literal(node)) return node.text;
  if (ts.isComputedPropertyName(node) && literal(node.expression)) return node.expression.text;
  return undefined;
}
function visit(node) {
  const parent = node.parent;
  if (parent && !ts.isPropertyAccessExpression(parent) && parent.name === node && (ts.isIdentifier(node) || ts.isPrivateIdentifier(node) || literal(node))) {
    // ImportSpecifier.name is the local binding; propertyName belongs to the exporter.
    // This also covers declarations, parameters, object keys and member definitions.
    record('symbol', node.text, node);
  }
  if (node.name && ts.isComputedPropertyName(node.name) && literal(node.name.expression)) {
    record('field', node.name.expression.text, node.name.expression);
  }
  if (node.name && isResource(propertyName(node.name)) && literal(node.initializer)) {
    record('resource', node.initializer.text, node.initializer);
  }
  if (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.EqualsToken) {
    const target = node.left;
    const name = ts.isIdentifier(target) ? target.text : ts.isPropertyAccessExpression(target) ? target.name.text : ts.isElementAccessExpression(target) ? propertyName(target.argumentExpression) : undefined;
    if (ts.isElementAccessExpression(target) && literal(target.argumentExpression)) {
      record('field', target.argumentExpression.text, target.argumentExpression);
    }
    if (isResource(name) && literal(node.right)) record('resource', node.right.text, node.right);
    if (ts.isPropertyAccessExpression(target)) record('field', target.name.text, target.name);
  }
  ts.forEachChild(node, visit);
}
visit(source);
process.stdout.write(JSON.stringify(names));
