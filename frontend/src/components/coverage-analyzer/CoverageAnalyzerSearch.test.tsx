import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CoverageAnalyzerSearch } from './CoverageAnalyzerSearch';

function setup(overrides = {}) {
  const onSearch = vi.fn();
  const onError = vi.fn();
  render(
    <CoverageAnalyzerSearch
      onSearch={onSearch}
      onError={onError}
      lastSlots={null}
      {...overrides}
    />
  );
  return { onSearch, onError };
}

describe('CoverageAnalyzerSearch', () => {
  it('renders 6 slots', () => {
    setup();
    for (let i = 1; i <= 6; i++) {
      expect(screen.getByText(`slot ${i}`)).toBeInTheDocument();
    }
  });

  it('type inputs are disabled when slot not enabled', () => {
    setup();
    const type1Inputs = screen.getAllByLabelText('type 1');
    expect(type1Inputs[0]).toBeDisabled();
  });

  it('type inputs are enabled after enabling slot', async () => {
    setup();
    const user = userEvent.setup();
    const checkboxes = screen.getAllByRole('checkbox', { name: /enabled/i });
    await user.click(checkboxes[0]);
    const type1Inputs = screen.getAllByLabelText('type 1');
    expect(type1Inputs[0]).not.toBeDisabled();
  });

  it('calls onError when no slots are enabled', async () => {
    const { onError } = setup();
    const user = userEvent.setup();
    await user.click(screen.getByText('Scan'));
    expect(onError).toHaveBeenCalledWith('Enable at least one slot and enter a type.');
  });

  it('calls onError when slot enabled but no type entered', async () => {
    const { onError } = setup();
    const user = userEvent.setup();
    const checkboxes = screen.getAllByRole('checkbox', { name: /enabled/i });
    await user.click(checkboxes[0]);
    await user.click(screen.getByText('Scan'));
    expect(onError).toHaveBeenCalledWith('Enable at least one slot and enter a type.');
  });

  it('calls onSearch with correct slots when valid', async () => {
    const { onSearch } = setup();
    const user = userEvent.setup();
    const checkboxes = screen.getAllByRole('checkbox', { name: /enabled/i });
    await user.click(checkboxes[0]);
    const type1Inputs = screen.getAllByLabelText('type 1');
    await user.type(type1Inputs[0], 'fire');
    await user.click(screen.getByText('Scan'));
    expect(onSearch).toHaveBeenCalledWith(['fire']);
  });

  it('combines type1 and type2 with hyphen', async () => {
    const { onSearch } = setup();
    const user = userEvent.setup();
    const checkboxes = screen.getAllByRole('checkbox', { name: /enabled/i });
    await user.click(checkboxes[0]);
    const type1Inputs = screen.getAllByLabelText('type 1');
    const type2Inputs = screen.getAllByLabelText('type 2');
    await user.type(type1Inputs[0], 'water');
    await user.type(type2Inputs[0], 'ground');
    await user.click(screen.getByText('Scan'));
    expect(onSearch).toHaveBeenCalledWith(['water-ground']);
  });

  it('calls onError when params unchanged', async () => {
    const { onError } = setup({ lastSlots: ['fire'] });
    const user = userEvent.setup();
    const checkboxes = screen.getAllByRole('checkbox', { name: /enabled/i });
    await user.click(checkboxes[0]);
    const type1Inputs = screen.getAllByLabelText('type 1');
    await user.type(type1Inputs[0], 'fire');
    await user.click(screen.getByText('Scan'));
    expect(onError).toHaveBeenCalledWith('Request not sent: Search parameters unchanged.');
  });
});
