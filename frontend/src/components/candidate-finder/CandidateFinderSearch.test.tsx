import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CandidateFinderSearch } from './CandidateFinderSearch';

function setup(overrides = {}) {
  const onSearch = vi.fn();
  const onError = vi.fn();
  render(
    <CandidateFinderSearch
      onSearch={onSearch}
      onError={onError}
      lastParams={null}
      {...overrides}
    />
  );
  return { onSearch, onError };
}

describe('CandidateFinderSearch', () => {
  it('renders all filter sections', () => {
    setup();
    expect(screen.getByText('special pokemon')).toBeInTheDocument();
    expect(screen.getByText('move')).toBeInTheDocument();
    expect(screen.getByText('stats')).toBeInTheDocument();
    expect(screen.getByText('desired type')).toBeInTheDocument();
    expect(screen.getByText("Catch 'em all!")).toBeInTheDocument();
  });

  it('calls onSearch with move param when move enabled and filled', async () => {
    const { onSearch } = setup();
    const user = userEvent.setup();

    await user.click(screen.getAllByRole('checkbox', { name: /enabled/i })[0]);
    await user.type(screen.getByLabelText('move name'), 'flamethrower');
    await user.click(screen.getByText("Catch 'em all!"));

    expect(onSearch).toHaveBeenCalledWith(expect.objectContaining({ move: 'flamethrower' }));
  });

  it('converts spaces to underscores in move name', async () => {
    const { onSearch } = setup();
    const user = userEvent.setup();

    await user.click(screen.getAllByRole('checkbox', { name: /enabled/i })[0]);
    await user.type(screen.getByLabelText('move name'), 'fire spin');
    await user.click(screen.getByText("Catch 'em all!"));

    expect(onSearch).toHaveBeenCalledWith(expect.objectContaining({ move: 'fire_spin' }));
  });

  it('calls onError for float stat input', async () => {
    const { onError } = setup();
    const user = userEvent.setup();

    // enable stats
    await user.click(screen.getAllByRole('checkbox', { name: /enabled/i })[1]);
    await user.type(screen.getByLabelText('minimum value', { selector: '#min-primary' }), '1.5');
    await user.click(screen.getByText("Catch 'em all!"));

    expect(onError).toHaveBeenCalledWith('Expected integer, got float: 1.5');
  });

  it('calls onError for stat value out of range', async () => {
    const { onError } = setup();
    const user = userEvent.setup();

    await user.click(screen.getAllByRole('checkbox', { name: /enabled/i })[1]);
    await user.type(screen.getByLabelText('minimum value', { selector: '#min-primary' }), '999');
    await user.click(screen.getByText("Catch 'em all!"));

    expect(onError).toHaveBeenCalledWith('Stat field must be a number between 1 and 255');
  });

  it('calls onError when params unchanged', async () => {
    const lastParams = { include_legendary: false, include_mythical: false, include_ultra_beasts: false };
    const { onError } = setup({ lastParams });
    const user = userEvent.setup();

    await user.click(screen.getByText("Catch 'em all!"));

    expect(onError).toHaveBeenCalledWith('Request not sent: Search parameters unchanged.');
  });

  it('move input is disabled when move not enabled', () => {
    setup();
    expect(screen.getByLabelText('move name')).toBeDisabled();
  });

  it('stat inputs are disabled when stats not enabled', () => {
    setup();
    expect(screen.getByLabelText('minimum value', { selector: '#min-primary' })).toBeDisabled();
  });
});
